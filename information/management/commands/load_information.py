__author__ = 'dheerendra'

from django.core.management.base import BaseCommand
from information.serializers import ContactSerializer, ClubSerializer, DepartmentSerializer, EmergencyContactSerializer
from django.conf import settings
import json
import os


class Command(BaseCommand):
    can_import_settings = True
    help = "Load JSON information file"

    def load_model(self, model_serializer, json_file):
        model_name = model_serializer.Meta.model.__name__
        model_type = model_serializer.Meta.model
        if not os.path.isfile(json_file):
            self.stderr.write("File Not Found. Error in retrieving file %s" % json_file)
        else:
            with open(json_file) as data_file:
                data = json.load(data_file)
            for datum in data:
                model = model_serializer(data=datum)
                if model.is_valid():
                    try:
                        model_type.objects.get(pk=datum['id'])
                    except model_type.DoesNotExist:
                        model.save()
                else:
                    self.stderr.write("\nCannot load invalid data into model %s from file %s with pk %s" % (
                        model_name, json_file, datum['id']))
                    for error in model.errors:
                        self.stderr.write("  %s" % error)
                        for msg in model.errors[error]:
                            self.stderr.write("   * %s" % msg)
            self.stdout.write("Loaded %ss into db" % model_name)

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        self.load_model(ContactSerializer, os.path.join(base_dir, "information/init_data/contacts.json"))
        self.load_model(ClubSerializer, os.path.join(base_dir, "information/init_data/clubs.json"))
        self.load_model(DepartmentSerializer, os.path.join(base_dir, "information/init_data/department.json"))
        self.load_model(EmergencyContactSerializer,
                        os.path.join(base_dir, "information/init_data/emergency_contacts.json"))
