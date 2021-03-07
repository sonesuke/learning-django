# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ManagedObject


class VersionTests(TestCase):
    def test_bump_version(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")
        project.bump_version(force=True)
        self.assertEqual(len(project.version_ids()), 2)

    def test_managed_save(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")
        project.bump_version(force=True)
        newest_object = ManagedObject.objects.filter_project(project=project).all()
        self.assertEqual(newest_object.count(), 1)
        newest_object.managed_save()
        self.assertEqual(ManagedObject.objects.filter_project(project=project).count(), 1)
        self.assertEqual(ManagedObject.objects.filter(project_id=project.project_id).count(), 2)

    def test_managed_delete(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")
        project.bump_version(force=True)
        newest_object = ManagedObject.objects.filter_project(project=project).all()
        newest_object.managed_delete()
        self.assertEqual(ManagedObject.objects.filter(project_id=project.project_id).count(), 1)
        self.assertEqual(ManagedObject.objects.filter_project(project=project).count(), 0)
