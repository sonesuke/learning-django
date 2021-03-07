# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, History, ManagedObject, ApplicationObject


class ProjectModelTests(TestCase):
    def setUp(self):
        # Clear all objects.
        Project.objects.all().delete()
        History.objects.all().delete()
        ApplicationObject.objects.all().delete()
        ManagedObject.objects.all().delete()

    def test_create_project(self):
        # Create a project.
        project = Project.objects.create()

        # First version is one, and its count is one.
        self.assertEqual(project.version_id(), 1)
        self.assertEqual(project.version_ids(), [1])
