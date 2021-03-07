# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, History, ManagedObject, ApplicationObject


class VersionTests(TestCase):
    def setUp(self):
        # Clear all objects.
        Project.objects.all().delete()
        History.objects.all().delete()
        ApplicationObject.objects.all().delete()
        ManagedObject.objects.all().delete()

    def test_bump_version(self):
        # Create a project.
        project = Project.objects.create()

        # Bump version.
        project.bump_version(force=True)

        # the project should have two versions. And latest version is 2.
        self.assertEqual(project.version_id(), 2)
        self.assertEqual(project.version_ids(), [1, 2])

    def test_managed_save(self):
        # Create a project and add a managed object.
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")

        # Bump version.
        project.bump_version(force=True)

        # Added managed object should bump version by the project bumping.
        self.assertEqual(ManagedObject.objects.filter_project(project=project).count(), 1)
        newest_object = ManagedObject.objects.filter_project(project=project).get()
        self.assertEqual(project.version_id(), 2)
        self.assertEqual(newest_object.version_id, 2)
        all_versions = ManagedObject.objects.filter(project_id=project.project_id, object_id=newest_object.object_id)
        self.assertEqual([object.version_id for object in all_versions], [1, 2])

        # Save the manged object.
        newest_object.value = "B"
        newest_object.managed_save()

        # Count of manged object is the same with before saving it.
        all_versions = ManagedObject.objects.filter(project_id=project.project_id, object_id=newest_object.object_id)
        self.assertEqual([object.version_id for object in all_versions], [1, 2])
        self.assertEqual([object.value for object in all_versions], ["A", "B"])

    def test_managed_delete(self):
        # Create a project and add a managed object.
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")

        # Bump version.
        project.bump_version(force=True)

        # Delete all object from current version.
        newest_object = ManagedObject.objects.filter_project(project=project).all()
        newest_object.managed_delete()

        # Current version object should be deleted.
        self.assertEqual(ManagedObject.objects.filter_project(project=project).count(), 0)

        # Old version object should be remaining.
        self.assertEqual(ManagedObject.objects.filter(project_id=project.project_id).count(), 1)
