from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .history import History
from .historian import HistorianMixIn

from typing import Any


class Project(models.Model, HistorianMixIn):
    project_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.project_id}_{self.version_id()}_{self.version_ids()}"


@receiver(pre_save, sender=Project)
def pre_create_project_hook(sender: Any, instance: Project, **kwargs: Any) -> None:
    if instance.project_id == 0:
        id_max = Project.objects.all().aggregate(models.Max("project_id"))["project_id__max"]
        instance.project_id = 1 if id_max is None else id_max + 1


@receiver(post_save, sender=Project)
def post_save_project_hook(sender: Any, instance: Project, created: bool, **kwargs: Any) -> None:
    if created:
        History.objects.create(project_id=instance.project_id)


@receiver(post_delete, sender=Project)
def post_delete_project_hook(sender: Any, instance: Project, **kwargs: Any) -> None:
    History.objects.filter(project_id=instance.project_id).delete()
