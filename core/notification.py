import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.utils import DNS_NAME


def send_mail(subject, text_msg, from_email, to_email_list):

    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.ehlo()
    server.esmtp_features['auth'] = 'LOGIN PLAIN'
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    mail = MIMEMultipart("alternative")
    mail['Subject'] = subject
    mail['From'] = from_email
    mail.attach(MIMEText(text_msg, 'plain'))

    for to_email in to_email_list:
        mail['To'] = to_email
        server.sendmail(from_email, to_email, mail.as_string())


class IITBEmailBackend(EmailBackend):

    def open(self):
        """
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        connection_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
        # If local_hostname is not specified, socket.getfqdn() gets used.
        # For performance, we use the cached FQDN for local_hostname.
        connection_params = {'local_hostname': DNS_NAME.get_fqdn()}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout
        if self.use_ssl:
            connection_params.update({
                'keyfile': self.ssl_keyfile,
                'certfile': self.ssl_certfile,
            })
        try:
            self.connection = connection_class(self.host, self.port, **connection_params)

            # TLS/SSL are mutually exclusive, so only attempt TLS over
            # non-secure connections.
            self.connection.starttls()
            self.connection.ehlo()
            self.connection.esmtp_features['auth'] = 'LOGIN PLAIN'
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise