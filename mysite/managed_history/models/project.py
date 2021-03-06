from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .history import History
from typing import List, Any


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Project {self.id}_{self.versions()}"

    def version(self) -> History:
        return History.objects.filter(project=self).last()  # type: ignore

    def versions(self) -> List[History]:
        return [history for history in History.objects.filter(project=self).order_by("id")]

    def bump_version(self) -> None:
        History.objects.create(project=self)


@receiver(post_save, sender=Project)
def create_history(sender: Any, instance: Project, created: bool, **kwargs: Any) -> None:
    if created:
        History.objects.create(project=instance)
