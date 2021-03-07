# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ManagedObject


class ManagedObjectModelTests(TestCase):
    def test_create_managed_object(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")

    def test_fetch_newest_managed_object(self):
        Project.objects.all().delete()
        project = Project.objects.create()
        ManagedObject.objects.managed_create(project=project, value="A")
        objects = list(ManagedObject.objects.filter(project_id=project.project_id).all())
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].value, "A")
