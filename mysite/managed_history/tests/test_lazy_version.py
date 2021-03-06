# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ManagedObject, ApplicationObject


class VersionTests(TestCase):
    def test_bump_version(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")
        project.bump_version()
        ApplicationObject.objects.create(project=project)
        self.assertEqual(len(project.versions()), 1)
        project.bump_version()
        self.assertEqual(len(project.versions()), 2)

    def test_managed_save(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")
        self.assertEqual(len(project.versions()), 1)
        ApplicationObject.objects.create(project=project)
        ManagedObject.objects.filter_project(project=project).managed_save()
        self.assertEqual(len(project.versions()), 2)
        self.assertEqual(ManagedObject.objects.filter_project(project=project).count(), 1)
        self.assertEqual(ManagedObject.objects.filter(project=project).count(), 2)

    def test_managed_delete(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")
        self.assertEqual(len(project.versions()), 1)
        ApplicationObject.objects.create(project=project)
        ManagedObject.objects.filter_project(project=project).managed_delete()
        self.assertEqual(len(project.versions()), 2)
        self.assertEqual(ManagedObject.objects.filter_project(project=project).count(), 0)
        self.assertEqual(ManagedObject.objects.filter(project=project).count(), 1)
