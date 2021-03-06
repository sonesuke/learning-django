# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ManagedObject


class VersionTests(TestCase):
    def test_bump_version(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.create(project=project, value="A")
        project.bump_version()
        self.assertEqual(len(project.versions()), 2)
        self.assertEqual(ManagedObject.objects.filter(project=project).count(), 2)

    def test_bump_version_with_object(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.create(project=project, value="A")
        project.bump_version()
        newest_object = ManagedObject.objects.filter_project(project=project).all()
        self.assertEqual(newest_object.count(), 1)
        newest_object.managed_save()
        self.assertEqual(ManagedObject.objects.filter_project(project=project).count(), 1)
        self.assertEqual(ManagedObject.objects.filter(project=project).count(), 2)

    def test_managed_delete(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.create(project=project, value="A")
        project.bump_version()
        newest_object = ManagedObject.objects.filter_project(project=project).all()
        newest_object.filter(value="A").managed_delete()
        self.assertEqual(ManagedObject.objects.filter(project=project).count(), 1)
        newest_object = ManagedObject.objects.filter_project(project=project).all()
        self.assertEqual(newest_object.count(), 0)
