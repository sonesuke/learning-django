from django.db import models


class History(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
