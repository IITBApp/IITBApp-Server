import urllib2
import logging
from datetime import timedelta, datetime
import time
import re
import HTMLParser

from django.db import models
from django.contrib.auth.models import User
import feedparser
from django.utils import timezone
from django.utils.timezone import utc
import bs4

from signals import feed_entry_registered

logger = logging.getLogger(__name__)
non_image_html = re.compile(r'<img.*?/>')
jpg_png_image = re.compile(r'(jpe?g)|(png)$', re.IGNORECASE)
parser = HTMLParser.HTMLParser()


class FeedError(Exception):
    """
    An error occurred when fetching the feed

    If it was parsed despite the error, the feed and entries will be available:
        e.feed      None if not parsed
        e.entries   Empty list if not parsed
    """

    def __init__(self, *args, **kwargs):
        self.feed = kwargs.pop('feed', None)
        self.entries = kwargs.pop('entries', [])
        self.etag = kwargs.pop('etag', None)
        super(FeedError, self).__init__(*args, **kwargs)


class FeedConfig(models.Model):
    url = models.URLField(unique=True)
    etag = models.CharField(max_length=128, null=True, blank=True, default=None)
    updated = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    check_frequency = models.IntegerField(default=30)
    last_checked = models.DateTimeField(null=True, blank=True, default=datetime.fromtimestamp(0).replace(tzinfo=utc))

    def _fetch_feed(self):
        data = feedparser.parse(self.url, etag=self.etag)
        status = data.get('status', 200)
        feed = data.get('feed', None)
        etag = data.get('etag', None)
        entries = data.get('entries', [])

        if data.get('bozo') == 1:
            bozo = data['bozo_exception']
            if isinstance(bozo, urllib2.URLError):
                raise FeedError('URL error: %s' % bozo)

            # Unrecognised exception
            # Most of these will be SAXParseException, which doesn't convert
            # to a string cleanly, so explicitly mention the exception class
            raise FeedError(
                'Feed error: %s - %s' % (bozo.__class__.__name__, bozo),
                feed=feed, entries=entries, etag=etag
            )

        if status == 304:
            # Not Modified
            return None, [], None

        if status in (200, 302, 307):
            # Check for valid feed
            if feed is None:
                raise FeedError('(Feed Parsed) None Feed for %s' % self.title)
            if 'title' not in feed:
                raise FeedError('(Feed Parsed) title not present in %s' % self.title)
            if 'link' not in feed:
                raise FeedError('(Feed Parsed) link not present in %s' % self.link)

            # OK
            return feed, entries, etag

        if status in (404, 500, 502, 503, 504):
            raise FeedError('Temporary error %s' % status)

        # Feed gone
        if status == 410:
            raise FeedError('Feed has gone')

        # Unknown status
        raise FeedError('Unrecognised HTTP status %s' % status)

    def _process_tags(self, tags, feed_entry):
        categories = set()
        for tag in tags:
            term = tag.get('term', None)
            label = tag.get('label', None)
            scheme = tag.get('scheme', None)
            if term is None:
                logger.error("Invalid tag: Term not found. Entry: %s" % feed_entry.title)
                continue
            updated_values = ({'term': term, 'label': label, 'scheme': scheme})
            feed_category, created = FeedCategory.objects.update_or_create(feed_config=self, term=term,
                                                                           defaults=updated_values)
            if created:
                all_users = User.objects.all()
                feed_category.subscribers.add(*all_users)
            categories.add(feed_category)

        if not categories:
            # Adding None category if there is no category in feed entry
            categories.add(FeedCategory.objects.get(term='None', feed_config=self))
        old_categories = set(feed_entry.categories.all())
        categories_to_add = categories - old_categories
        # New categories to add. Important in case of feed entry is updated
        categories_to_remove = old_categories - categories
        # Old categories which have to be removed. Important in case of feed entry is updated
        if categories_to_add:
            feed_entry.categories.add(*categories_to_add)
        if categories_to_remove:
            feed_entry.categories.remove(*categories_to_remove)
        feed_entry.categories.add(*categories)

    def _process_feed_entries(self, raw_feed_entries):
        logger.info("Raw feed entries processing started for feed %d" % self.id)
        for raw_feed_entry in raw_feed_entries:
            raw_feed_entry_id = raw_feed_entry.id
            created = False
            try:
                feed_entry = FeedEntry.objects.get(entry_id=raw_feed_entry_id)
                entry_updated = datetime.fromtimestamp(time.mktime(raw_feed_entry.updated_parsed)).replace(tzinfo=utc)
                if feed_entry.updated == entry_updated:
                    continue
            except FeedEntry.DoesNotExist:
                feed_entry = FeedEntry(entry_id=raw_feed_entry_id)
                created = True

            soup = bs4.BeautifulSoup(raw_feed_entry.content[0].value, 'html.parser')

            images = [image['src'] for image in soup.findAll('img', {'src': jpg_png_image}) if
                      image['src'].startswith(self.link)]
            images = ",".join(images)

            feed_entry.feed_config = self
            feed_entry.title = parser.unescape(raw_feed_entry.title)
            feed_entry.link = raw_feed_entry.link
            feed_entry.updated = raw_feed_entry.updated
            feed_entry.published = raw_feed_entry.published
            feed_entry.content = non_image_html.sub('', raw_feed_entry.content[0].value)
            feed_entry.author = raw_feed_entry.author
            feed_entry.images = images
            feed_entry.save()
            self._process_tags(raw_feed_entry.tags, feed_entry)
            feed_entry_registered.send(sender=FeedEntry, instance=feed_entry, created=created)
        logger.info("Raw feed entries processing finished for feed %d" % self.id)

    def check_feeds(self, force=False):
        next_schedule = self.last_checked + timedelta(minutes=self.check_frequency)
        now = timezone.now()
        if not force and next_schedule > now:
            return

        try:
            feed, raw_feed_entries, etag = self._fetch_feed()
        except FeedError as e:
            logger.error("Error: %s" % e)
            feed = e.feed
            raw_feed_entries = e.entries
            etag = e.etag

        self.last_checked = now
        self.save()
        self.refresh_from_db()

        if not feed:
            return

        logger.info("Feeds fetched")

        updated = feed.get(
            'updated_parsed',
            feed.get('published_parsed', self.updated),
        )
        if updated:
            updated = datetime.fromtimestamp(
                time.mktime(updated)
            ).replace(tzinfo=utc)

        self.etag = etag
        self.updated = updated
        self.title = feed.get('title', self.title)
        self.link = feed.get('link', self.link)
        self.save()
        self.refresh_from_db()
        self._process_feed_entries(raw_feed_entries)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return ''


class FeedCategory(models.Model):
    term = models.CharField(max_length=128, db_index=True)
    scheme = models.URLField(null=True, blank=True)
    label = models.CharField(max_length=128, null=True, blank=True)
    feed_config = models.ForeignKey(FeedConfig, related_name='categories')
    subscribers = models.ManyToManyField(User, related_name='feed_subscriptions')

    def __unicode__(self):
        return self.term

    class Meta:
        unique_together = ('feed_config', 'term')


class FeedEntry(models.Model):
    entry_id = models.CharField(max_length=200, db_index=True)
    feed_config = models.ForeignKey(FeedConfig, related_name='entries')
    title = models.CharField(max_length=128)
    link = models.URLField()
    updated = models.DateTimeField()
    published = models.DateTimeField()
    content = models.TextField()
    author = models.CharField(max_length=64)
    images = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(FeedCategory, related_name='entries')

    def __unicode__(self):
        return self.title


class FeedEntryLike(models.Model):
    entry = models.ForeignKey(FeedEntry, related_name='likes')
    user = models.ForeignKey(User)


class FeedEntryView(models.Model):
    entry = models.ForeignKey(FeedEntry, related_name='views')
    user = models.ForeignKey(User)
    view_count = models.IntegerField(default=0)

    def add_view(self):
        self.view_count += 1
        self.save()


class Feed(models.Model):
    guid = models.CharField(max_length=128)
    user = models.ForeignKey(User)

    class Meta:
        abstract = True


class FeedLike(Feed):
    pass


class FeedView(Feed):
    view_count = models.IntegerField(default=0)

    def add_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
