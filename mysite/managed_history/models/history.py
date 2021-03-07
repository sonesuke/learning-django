from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from typing import Any

from .managed_object import ManagedObject


class History(models.Model):
    version_id = models.IntegerField(default=0)
    project_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["version_id", "project_id"], name="History id unique"),
        ]

    def __str__(self) -> str:
        return f"{self.project_id}_{self.version_id}"


@receiver(pre_save, sender=History)
def pre_save_history_hook(sender: Any, instance: History, **kwargs: Any) -> None:
    if instance.version_id == 0:
        id_max = History.objects.filter(project_id=instance.project_id).aggregate(models.Max("version_id"))[
            "version_id__max"
        ]
        instance.version_id = 1 if id_max is None else id_max + 1


@receiver(post_delete, sender=History)
def post_delete_history_hook(sender: Any, instance: History, **kwargs: Any) -> None:
    ManagedObject.objects.filter(project_id=instance.project_id, version_id=instance.version_id).delete()
