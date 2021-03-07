# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ApplicationObject


class VersionTests(TestCase):
    def test_cleanup(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        project.cleanup()
        self.assertEqual(len(project.versions()), 1)
        project.bump_version(force=True)
        self.assertEqual(len(project.versions()), 2)
        project.cleanup()
        self.assertEqual(len(project.versions()), 1)
        ApplicationObject.objects.create(project=project)
        project.bump_version(force=True)
        self.assertEqual(len(project.versions()), 2)
        project.cleanup()
        self.assertEqual(len(project.versions()), 2)
