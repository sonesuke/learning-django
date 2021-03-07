from django.db import models


from django.db import transaction
from typing import List, Any


class HistorianMixIn:
    def _project_id(self) -> int:
        return self.project_id  # type: ignore

    def version_id(self) -> int:
        from .history import History

        return History.objects.filter(project_id=self._project_id()).last().version_id  # type: ignore

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

    def bump_version(self, abandoned_object: Any = None, force: bool = None) -> int:
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
                object.version_id = history.version_id
                object.pk = None
                object.save(force_insert=True)

            return history.version_id  # type: ignore


class ApplicationObjectQuerySet(models.QuerySet):
    pass

class ApplicationObjectManager(models.Manager.from_queryset(ApplicationObjectQuerySet)) :  # type: ignore
    def managed_create(self, project: Any, **kwargs: Any) -> 'ApplicationObject':
        kwargs["project_id"] = project.project_id
        if "version_id" not in kwargs:
            kwargs["version_id"] = project.version_id()
        return self.create(**kwargs)  # type: ignore


class ManagedObjectMixIn:
    def _project(self, project_id: int) -> HistorianMixIn:
        from .project import Project

        return Project.objects.filter(project_id=project_id).get()  # type: ignore

    def managed_save(self, **kwargs: Any) -> None:
        project_id = kwargs["project_id"] if "project_id" in kwargs else self.project_id #type ignore
        newest_version_id = self._project(project_id).bump_version(abandoned_object=self)
        bumping = self.version_id != newest_version_id  # type: ignore
        if bumping:
            self.pk = None
            self.version_id = newest_version_id  # type: ignore
        kwargs["force_insert"] = bumping
        self.save(**kwargs)  # type: ignore

    def managed_delete(self, **kwargs: Any) -> None:
        newest_version_id = self._project(self.project_id).bump_version(abandoned_object=self) # type: ignore
        if self.version_id == newest_version_id:
            self.delete(**kwargs)  # type: ignore


class ManagedObjectQuerySet(models.QuerySet):
    def filter_application(self, application: Any) -> models.QuerySet:
        return self.filter(version_id=application.version_id)

    def filter_project(self, project: Any) -> models.QuerySet:
        return self.filter(project_id=project.project_id, version_id=project.version_id())

    def managed_delete(self) -> None:
        [item.managed_delete() for item in self.all()]

    def managed_save(self) -> None:
        [item.managed_save() for item in self.all()]


class ManagedObjectQueryManager(models.Manager.from_queryset(ManagedObjectQuerySet)):  # type: ignore

    def managed_create(self, project: Any, **kwargs: Any) -> 'ManagedObject':
        kwargs["project_id"] = project.project_id
        if  "version_id" not in kwargs:
            kwargs["version_id"] = project.version_id()
        return self.create(**kwargs)  # type: ignore
