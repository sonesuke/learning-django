# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ApplicationObject, ManagedObject


class ApplicationObjectModelTests(TestCase):
    def test_create_application_object(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ApplicationObject.objects.create(project=project)

    def test_watching_managed_object(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.create(project=project, value="A")
        application = ApplicationObject.objects.create(project=project)
        objects = list(ManagedObject.objects.filter_application(application=application).all())
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].value, "A")
