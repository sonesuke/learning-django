# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ManagedObject


class ManagedObjectModelTests(TestCase):
    def test_create_managed_object(self):
        Project.objects.all().delete()
        project = Project()
        project.save()
        managed_object = ManagedObject(project=project, value="A")
        managed_object.save()
