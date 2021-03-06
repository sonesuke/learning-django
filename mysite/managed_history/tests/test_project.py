# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project


class ProjectModelTests(TestCase):
    def test_create_project(self):
        Project.objects.all().delete()
        project = Project()
        project.save()
        assert project

    def test_create_project_with_history(self):
        Project.objects.all().delete()
        project = Project()
        project.save()
        self.assertEqual(project.version(), max(project.versions()))

    def test_bump_version(self):
        Project.objects.all().delete()
        project = Project()
        project.save()
        project.bump_version()
        self.assertEqual(len(project.versions()), 2)
