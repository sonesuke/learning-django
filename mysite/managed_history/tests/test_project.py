# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..service import ProjectService


class ProjectModelTests(TestCase):
    def test_create_project(self):
        ProjectService.delete_all()
        ProjectService.create()
        ret = ProjectService.fetch_all()
        self.assertEqual(len(ret), 1)

    def test_delete_project(self):
        ProjectService.create()
        ProjectService.delete_all()
        ret = ProjectService.fetch_all()
        self.assertEqual(len(ret), 0)
