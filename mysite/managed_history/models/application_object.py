from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from typing import Any


class ApplicationObject(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=False)
    version = models.ForeignKey("History", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"ApplicationObject {self.project}_{self.version}"


@receiver(pre_save, sender=ApplicationObject)
def create_history(sender: Any, instance: ApplicationObject, **kwargs: Any) -> None:
    if instance.version is None:
        instance.version = instance.project.version()
