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

    def test_lazy_bump_version(self):
        # Create a project with a managed object.
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")

        # Bump version.
        project.bump_version()

        # Bumping doesn't happen by no application watching this version.
        self.assertEqual(project.version_id(), 1)

        # Add application for watching.
        ApplicationObject.objects.managed_create(project=project)

        # Bump version.
        project.bump_version()

        # Bumping happens by an application watching this version.
        self.assertEqual(project.version_id(), 2)

    def test_lazy_managed_save(self):
        # Create a project with a managed object.
        project = Project.objects.create()
        object = ManagedObject.objects.managed_create(project=project, value="A")

        # Add application for watching.
        ApplicationObject.objects.managed_create(project=project)

        # Bumping happened by managed saving of objects.
        ManagedObject.objects.filter_project(project=project).managed_save()

        # The version should be bumping.
        self.assertEqual(project.version_id(), 2)

        # The object should has two versions.
        all_versions = ManagedObject.objects.filter(project_id=project.project_id, object_id=object.object_id)
        self.assertEqual([object.version_id for object in all_versions], [1, 2])

    def test_lazy_managed_delete(self):
        # Create a project with a managed object.
        project = Project.objects.create()
        object = ManagedObject.objects.managed_create(project=project, value="A")

        # Add application for watching.
        ApplicationObject.objects.managed_create(project=project)

        # Bumping happened by managed deleting of objects.
        ManagedObject.objects.filter_project(project=project).managed_delete()

        # The version should be bumping.
        self.assertEqual(project.version_id(), 2)

        # The object should has one version.
        all_versions = ManagedObject.objects.filter(project_id=project.project_id, object_id=object.object_id)
        self.assertEqual([object.version_id for object in all_versions], [1])
