from .models import Project
from typing import List


class ProjectService(object):
    @staticmethod
    def create() -> None:
        project = Project()
        project.save()

    @staticmethod
    def delete_all() -> None:
        Project.objects.all().delete()

    @staticmethod
    def fetch_all() -> List[Project]:
        return list(Project.objects.all())

    @staticmethod
    def fetch() -> Project:
        return Project.objects.last()  # type: ignore
