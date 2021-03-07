from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from .history import History
from .application_object import ApplicationObject

from typing import List, Any


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id}_{self.version()}_{self.versions()}"

    def version(self) -> History:
        return History.objects.filter(project=self).last()  # type: ignore

    def versions(self) -> List[History]:
        return [history for history in History.objects.filter(project=self).order_by("id")]

    def cleanup(self) -> None:
        living_versions = self.versions()
        used_versions = [a.version for a in ApplicationObject.objects.filter(project=self)]
        for v in living_versions[:-1]:
            if v not in used_versions:
                v.delete()

    def bump_version(self, abandoned_object: Any = None, force: bool = None) -> History:
        from .managed_object import ManagedObject

        with transaction.atomic():
            if ApplicationObject.objects.filter(version=self.version()).count() == 0 and not force:
                return self.version()  # type: ignore
            objects = ManagedObject.objects.filter_project(project=self).all()
            history = History.objects.create(project=self)
            for object in objects:
                if object == abandoned_object:
                    continue
                object.version = history
                object.pk = None
                object.save(force_insert=True)
            return history  # type: ignore


@receiver(post_save, sender=Project)
def create_history(sender: Any, instance: Project, created: bool, **kwargs: Any) -> None:
    if created:
        History.objects.create(project=instance)
