# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, History, ManagedObject, ApplicationObject


class ApplicationObjectModelTests(TestCase):
    def setUp(self):
        # Clear all objects.
        Project.objects.all().delete()
        History.objects.all().delete()
        ApplicationObject.objects.all().delete()
        ManagedObject.objects.all().delete()

    def test_create_application_object(self):
        # Create a project with a managed object.
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")

        # Add an application.
        application = ApplicationObject.objects.managed_create(project=project)

        # Application should be able to watch the managed object.
        objects = ManagedObject.objects.filter_application(application=application).all()
        self.assertEqual([object.value for object in objects], ["A"])
