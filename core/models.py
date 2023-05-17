from django.db import models
from django.conf import settings


class Status(models.Model):
    status = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.status


class KanbanModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status =  models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
