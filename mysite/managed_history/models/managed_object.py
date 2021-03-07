from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from typing import Any
from .historian import ManagedObjectMixIn, ManagedObjectQueryManager


class ManagedObject(models.Model, ManagedObjectMixIn):
    objects = ManagedObjectQueryManager()

    object_id = models.IntegerField(default=0)
    project_id = models.IntegerField(default=0)
    version_id = models.IntegerField(default=0)
    value = models.CharField(max_length=24)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["object_id", "project_id", "version_id"], name="ManagedObject id unique"),
        ]

    def __str__(self) -> str:
        return f"{self.project_id}_{self.version_id}_{self.object_id}: {self.value}"


@receiver(pre_save, sender=ManagedObject)
def pre_save_management_object_hook(sender: Any, instance: ManagedObject, **kwargs: Any) -> None:
    if instance.object_id == 0:
        id_max = ManagedObject.objects.filter(project_id=instance.project_id).aggregate(models.Max("object_id"))[
            "object_id__max"
        ]
        instance.object_id = 1 if id_max is None else id_max + 1
