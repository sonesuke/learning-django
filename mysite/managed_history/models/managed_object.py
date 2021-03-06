from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from typing import Any


class ManagedObject(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=False)
    version = models.ForeignKey("History", on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=24)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"ManagedObject {self.project}_{self.version}: {self.value}"


@receiver(pre_save, sender=ManagedObject)
def create_history(sender: Any, instance: ManagedObject, **kwargs: Any) -> None:
    if instance.version is None:
        instance.version = instance.project.version()
