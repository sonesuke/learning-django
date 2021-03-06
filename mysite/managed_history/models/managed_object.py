from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from typing import Any
from .application_object import ApplicationObject
from .project import Project


class ApplicationQuerySet(models.QuerySet):
    def filter_application(self, application: ApplicationObject) -> models.QuerySet:
        return self.filter(version=application.version)

    def filter_project(self, project: Project) -> models.QuerySet:
        return self.filter(version=project.version())


class ApplicationQueryManager(models.Manager.from_queryset(ApplicationQuerySet)):  # type: ignore
    pass


class ManagedObject(models.Model):
    objects = ApplicationQueryManager()

    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=False)
    version = models.ForeignKey("History", on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=24)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.project}_{self.version}: {self.value}"

    def managed_save(self, **kwargs: Any) -> None:
        newest_version = self.project.version()
        bumping = self.version != newest_version
        if bumping:
            self.version = newest_version
            self.pk = None
        kwargs["force_insert"] = bumping
        super(ManagedObject, self).save(**kwargs)


@receiver(pre_save, sender=ManagedObject)
def create_history(sender: Any, instance: ManagedObject, **kwargs: Any) -> None:
    if instance.version is None:
        instance.version = instance.project.version()
