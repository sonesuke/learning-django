# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, History, ManagedObject, ApplicationObject


class CleanupTest(TestCase):
    def setUp(self):
        # Clear all objects.
        Project.objects.all().delete()
        History.objects.all().delete()
        ApplicationObject.objects.all().delete()
        ManagedObject.objects.all().delete()

    def test_cleanup(self):
        # Create a project.
        project = Project.objects.create()
        self.assertEqual(project.version_id(), 1)

        # Clean up versions.
        project.cleanup()

        # Current version should be the same, because there is newest version only.
        self.assertEqual(project.version_id(), 1)

        # Bumping version.
        project.bump_version(force=True)

        # The project should have two version, and newest is 2.
        self.assertEqual(project.version_ids(), [1, 2])

        # Clean up versions.
        project.cleanup()

        # The version 1 should be deleted, because no application watching it and it is not newest one.
        self.assertEqual(project.version_ids(), [2])

        # Add application for watching the version 2.
        ApplicationObject.objects.managed_create(project=project)

        # Bumping version.
        project.bump_version(force=True)

        # The project should get new version.
        self.assertEqual(project.version_ids(), [2, 3])

        # clean up versions.
        project.cleanup()

        # The version 2 should NOT be deleted, because the application watching it.
        self.assertEqual(project.version_ids(), [2, 3])
