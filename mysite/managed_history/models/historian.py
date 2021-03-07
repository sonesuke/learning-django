from django.db import models


from django.db import transaction
from typing import List, Any, Optional


def _replace_version(managed_object: 'models.ManagedObject', new_version_id: int) -> None:
    managed_object.pk = None
    managed_object.version_id = new_version_id


class HistorianMixIn:
    def _project_id(self) -> int:
        return self.project_id  # type: ignore

    def version_id(self) -> int:
        return max(self.version_ids())

    def version_ids(self) -> List[int]:
        from .history import History

        return [history.version_id for history in History.objects.filter(project_id=self._project_id()).order_by("id")]

    def cleanup(self) -> None:
        from .history import History
        from .application_object import ApplicationObject

        with transaction.atomic():
            living_version_ids = self.version_ids()
            used_versions_ids = [a.version_id for a in ApplicationObject.objects.filter(project_id=self._project_id())]
            for v in living_version_ids[:-1]:
                if v not in used_versions_ids:
                    History.objects.filter(project_id=self._project_id(), version_id=v).delete()

    def bump_version(self, abandoned_object: Optional['models.ManagedObject'] = None, force: bool = None) -> int:
        from .history import History
        from .application_object import ApplicationObject
        from .managed_object import ManagedObject

        with transaction.atomic():
            if ApplicationObject.objects.filter(version_id=self.version_id()).count() == 0 and not force:
                return self.version_id()  # type: ignore
            objects = ManagedObject.objects.filter_project(project=self).all()
            history = History.objects.create(project_id=self._project_id())

            for object in objects:
                if object == abandoned_object:
                    continue
                _replace_version(object, history.version_id)
                object.save(force_insert=True)

            return history.version_id  # type: ignore


class ApplicationObjectQuerySet(models.QuerySet):
    pass


class ApplicationObjectManager(models.Manager.from_queryset(ApplicationObjectQuerySet)):  # type: ignore
    def managed_create(self, project: 'models.Project', **kwargs: Any) -> 'models.ApplicationObject':
        kwargs["project_id"] = project.project_id
        if "version_id" not in kwargs:
            kwargs["version_id"] = project.version_id()
        return self.create(**kwargs)  # type: ignore


class ManagedObjectMixIn:
    def _project(self) -> 'models.Project':
        from .project import Project

        return Project.objects.filter(project_id=self.project_id).get()  # type: ignore

    def managed_save(self, **kwargs: Any) -> None:
        newest_version_id = self._project().bump_version(abandoned_object=self)
        if self.version_id != newest_version_id:  # type: ignore
            _replace_version(self, newest_version_id)
        self.save(**kwargs)  # type: ignore

    def managed_delete(self, **kwargs: Any) -> None:
        newest_version_id = self._project().bump_version(abandoned_object=self)
        if self.version_id == newest_version_id:  # type: ignore
            self.delete(**kwargs)  # type: ignore


class ManagedObjectQuerySet(models.QuerySet):
    def filter_application(self, application: 'models.AppcatlionObject') -> models.QuerySet:
        return self.filter(version_id=application.version_id)

    def filter_project(self, project: 'models.Project') -> models.QuerySet:
        return self.filter(project_id=project.project_id, version_id=project.version_id())

    def managed_delete(self, **kwargs: Any) -> None:
        [item.managed_delete(**kwargs) for item in self.all()]

    def managed_save(self, **kwargs: Any) -> None:
        [item.managed_save(**kwargs) for item in self.all()]


class ManagedObjectQueryManager(models.Manager.from_queryset(ManagedObjectQuerySet)):  # type: ignore
    def managed_create(self, project: 'models.Project', **kwargs: Any) -> 'models.ManagedObject':
        kwargs["project_id"] = project.project_id
        if "version_id" not in kwargs:
            kwargs["version_id"] = project.version_id()
        return self.create(**kwargs)  # type: ignore
