# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, History, ManagedObject, ApplicationObject


class ManagedObjectModelTests(TestCase):
    def setUp(self):
        # Clear all objects.
        Project.objects.all().delete()
        History.objects.all().delete()
        ApplicationObject.objects.all().delete()
        ManagedObject.objects.all().delete()

    def test_create_managed_object(self):
        # Create a project.
        project = Project.objects.create()

        # Create a managed object.
        ManagedObject.objects.managed_create(project=project, value="A")
        object = ManagedObject.objects.filter_project(project=project).get()
        self.assertEqual(object.version_id, 1)
        self.assertEqual(object.value, "A")
