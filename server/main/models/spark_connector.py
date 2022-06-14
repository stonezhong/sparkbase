from datetime import datetime
from django.db import models
from .datalake import DataLake
from django.contrib.auth.models import User

class SparkConnector(models.Model):
    id              = models.BigAutoField(primary_key=True)
    datalake        = models.ForeignKey(DataLake, on_delete=models.PROTECT, null=False, related_name="spark_connectors")
    name            = models.CharField(null=False, max_length=255, blank=False, unique=True)
    description     = models.TextField(null=False, blank=True)
    config          = models.TextField(null=False, blank=True)
    created_by      = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    created_at      = models.DateTimeField()
    is_active       = models.BooleanField(null=False)

    class Meta:
        unique_together = [
            ['datalake', 'name']
        ]

    @classmethod
    def create(cls, created_by:User, datalake:DataLake, name:str, description:str, config:str):
        """
        Create a datalake
        """
        spark_connector = SparkConnector(
            datalake=datalake,
            name=name,
            description=description,
            config=config,
            created_by=created_by,
            created_at=datetime.utcnow(),
            is_active=True,
        )
        spark_connector.save()
        return spark_connector
