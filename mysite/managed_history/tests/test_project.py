# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project


class ProjectModelTests(TestCase):
    def test_create_project(self):
        Project.objects.all().delete()
        Project.objects.create()

    def test_create_project_with_history(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        self.assertEqual(project.version_id(), max(project.version_ids()))
