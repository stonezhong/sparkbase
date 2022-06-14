from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, Group, Permission

class DataLake(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    name                = models.CharField(null=False, max_length=255, blank=False, unique=True)
    description         = models.TextField(null=False, blank=True)
    config              = models.TextField(null=False, blank=True)
    created_by          = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    created_at          = models.DateTimeField()
    is_active           = models.BooleanField(null=False)

    @classmethod
    def create(cls, created_by:User, name:str, description:str, config:str):
        """
        Create a datalake
        """
        datalake = DataLake(
            name=name,
            description=description,
            config=config,
            created_by=created_by,
            created_at=datetime.utcnow(),
            is_active=True,
        )
        datalake.save()

        datalake_admin = DataLakeAdmin(
            datalake = datalake,
            user = created_by
        )
        datalake_admin.save()

        return datalake


# Note: in django, there is no nested groups, group can only contain users

class DataLakeAdmin(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    datalake            = models.ForeignKey(DataLake, on_delete=models.PROTECT, null=False)
    user                = models.ForeignKey(User, on_delete=models.PROTECT, null=False, related_name='admins')

    class Meta:
        unique_together = [
            ['datalake', 'user']
        ]

class DataLakeUserPermission(models.Model):
    #########################################################
    # This model represent a user has a permission within a datalake
    #########################################################
    id                  = models.BigAutoField(primary_key=True)
    datalake            = models.ForeignKey(DataLake, on_delete=models.PROTECT, null=False)
    user                = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    permission          = models.ForeignKey(Permission, on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = [
            ['datalake', 'user', 'permission']
        ]

class DataLakeGroupPermission(models.Model):
    #########################################################
    # This model represent a group has a permission within a datalake
    #########################################################
    id                  = models.BigAutoField(primary_key=True)
    datalake            = models.ForeignKey(DataLake, on_delete=models.PROTECT, null=False)
    group               = models.ForeignKey(Group, on_delete=models.PROTECT, null=False)
    permission          = models.ForeignKey(Permission, on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = [
            ['datalake', 'group', 'permission']
        ]
