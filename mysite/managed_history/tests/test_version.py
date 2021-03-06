# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ManagedObject


class VersionTests(TestCase):
    def test_bump_version(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        project.bump_version()
        self.assertEqual(len(project.versions()), 2)

    def test_bump_version_with_object(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        object = ManagedObject.objects.create(project=project, value="A")
        project.bump_version()
        object.value = "B"
        object.managed_save()
        self.assertEqual(ManagedObject.objects.all().count(), 2)
        newest_object = ManagedObject.objects.filter_project(project=project).all()
        self.assertEqual(newest_object.count(), 1)
        self.assertEqual(newest_object[0].value, "B")

    def test_managed_delete(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        object = ManagedObject.objects.create(project=project, value="A")
        project.bump_version()
        object.value = "B"
        object.managed_save()
        self.assertEqual(ManagedObject.objects.all().count(), 2)
        newest_object = ManagedObject.objects.filter_project(project=project).all()
        self.assertEqual(newest_object.count(), 1)
        self.assertEqual(newest_object[0].value, "B")
