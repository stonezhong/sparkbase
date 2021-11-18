from datetime import datetime, timedelta
import uuid
from django.db import models
import pytz
import json

class AccessToken(models.Model):
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key                 = models.CharField(max_length=255, blank=False)
    content             = models.TextField(blank=True)
    create_time         = models.DateTimeField(null=False)
    expire_time         = models.DateTimeField(null=False)

    @classmethod
    def get_or_create_token(cls, key:str, content:dict, ttl:timedelta=timedelta(hours=1)):
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        access_tokens = AccessToken.objects.filter(key=key, expire_time__gt=now)
        if len(access_tokens) == 0:
            access_token = AccessToken(
                key = key,
                content = json.dumps(content),
                create_time = now,
                expire_time = now + ttl
            )
            access_token.save()
            return access_token
        
        assert len(access_tokens) == 1
        return access_tokens[0]
    
    @classmethod
    def get(cls, key:str):
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        access_tokens = AccessToken.objects.filter(key=key, expire_time__gt=now)
        if len(access_tokens) == 0:
            return None
        else:
            assert len(access_tokens) == 1
            return access_tokens[0]


    @classmethod
    def create(cls, key:str, content: dict, ttl:timedelta=timedelta(hours=1)):
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        access_token = AccessToken(
            key = key,
            content = json.dumps(content),
            create_time = now,
            expire_time = now + ttl
        )
        access_token.save()
        return access_token
    
    def update_content(self, content: dict):
        self.content = json.dumps(content)
        self.save()

