from django.db import models
from django_microservice_common.models import BaseModel


class File(BaseModel):
    name = models.CharField(null=True, max_length=100)
    description = models.CharField(null=True, max_length=255)

    class Meta:
        abstract = True
