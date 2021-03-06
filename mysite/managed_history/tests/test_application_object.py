# mypy: disallow_untyped_defs = False

from django.test import TestCase
from ..models import Project, ApplicationObject


class ApplicationObjectModelTests(TestCase):
    def test_create_application_object(self):
        Project.objects.all().delete()
        project = Project()
        project.save()
        application = ApplicationObject(project=project)
        application.save()
