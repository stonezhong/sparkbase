from enum import Enum
from django.db import models
from django.contrib.auth.models import User

class PermissionName(Enum):
    # a user has subscribed a dakalake
    SUBSCRIBE   = ("subscribe", "Subscribe")

    # such user can add user to datalake
    # remove user from datalake
    # change user permission to datalake
    USER_MANAGER  = ("user_manager", "User Manager")


class DataLake(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    name                = models.CharField(null=False, max_length=255, blank=False, unique=True)
    description         = models.TextField(null=False, blank=True)
    config              = models.TextField(null=False, blank=True)
    is_active           = models.BooleanField(null=False)

    @classmethod
    def create(cls, created_by:User, name:str, description:str, config:str):
        datalake = DataLake(name=name, description=description,config=config,is_active=True)
        datalake.save()

        subscribe_permission = Permission(
            datalake=datalake, 
            name=PermissionName.SUBSCRIBE.value[0],
            display_name=PermissionName.SUBSCRIBE.value[1],
        )
        subscribe_permission.save()

        user_manager_permission = Permission(
            datalake=datalake, 
            name=PermissionName.USER_MANAGER.value[0],
            display_name=PermissionName.USER_MANAGER.value[1],
        )
        user_manager_permission.save()

        permission_grant = PermissionGrant(user=created_by, datalake=datalake, permission=subscribe_permission)
        permission_grant.save()
        permission_grant = PermissionGrant(user=created_by, datalake=datalake, permission=user_manager_permission)
        permission_grant.save()

        return datalake



class Permission(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    datalake            = models.ForeignKey(DataLake, on_delete=models.PROTECT, null=False)
    name                = models.CharField(null=False, max_length=255, blank=False)
    display_name        = models.CharField(null=False, max_length=255, blank=False)

    class Meta:
        unique_together = [
            ['datalake', 'name']
        ]
    


class PermissionGrant(models.Model):
    """Represent a user has permission to a object with target_id in a datakale.
    If target_id is null, then the permission is not target specific
    """
    id                  = models.BigAutoField(primary_key=True)
    user                = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    datalake            = models.ForeignKey(DataLake, on_delete=models.PROTECT, null=False)
    permission          = models.ForeignKey(Permission, on_delete=models.PROTECT, null=False)
    target_id           = models.BigIntegerField(null=True)

    class Meta:
        unique_together = [
            ['user', 'datalake', 'permission', 'target_id']
        ]
