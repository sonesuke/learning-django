# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ApplicationObject


class CleanupTest(TestCase):
    def test_cleanup(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        project.cleanup()
        self.assertEqual(len(project.version_ids()), 1)
        project.bump_version(force=True)
        self.assertEqual(len(project.version_ids()), 2)
        project.cleanup()
        self.assertEqual(len(project.version_ids()), 1)
        ApplicationObject.objects.managed_create(project=project)
        project.bump_version(force=True)
        self.assertEqual(len(project.version_ids()), 2)
        project.cleanup()
        self.assertEqual(len(project.version_ids()), 2)
