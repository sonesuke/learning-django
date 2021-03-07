from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from typing import Any
from .historian import ApplicationObjectManager


class ApplicationObject(models.Model):
    objects = ApplicationObjectManager()

    application_id = models.IntegerField(default=0)
    project_id = models.IntegerField(default=0)
    version_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["application_id", "project_id", "version_id"],
                name="ApplicationObject id unique",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.project_id}_{self.version_id}_{self.application_id}"


@receiver(pre_save, sender=ApplicationObject)
def pre_save_hook(sender: Any, instance: ApplicationObject, **kwargs: Any) -> None:
    if instance.application_id == 0:
        id_max = ApplicationObject.objects.filter(project_id=instance.project_id).aggregate(
            models.Max("application_id")
        )["application_id__max"]
        instance.application_id = 1 if id_max is None else id_max + 1
