import uuid
from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=64)

    def __str__(self):
        return self.user_name
