from django.db import models
from django.contrib.auth.models import User
import uuid


class Support_query(models.Model):
    support_id = models.CharField(max_length=8, unique=True, editable=False, default="")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank = True, null = True)
    mobile = models.CharField(max_length = 13, null = True, blank = True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null = True, blank = True)
    call_time = models.DateTimeField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 25, default= "Processing")
    Issue_type = models.CharField(max_length = 255, blank = True, null = True)
    def save(self, *args, **kwargs):
        if not self.support_id:
            self.support_id = str(uuid.uuid4().int)[:8]
        super(Support_query, self).save(*args, **kwargs)

class Support_query_message(models.Model):
    message_id = models.CharField(max_length=8, unique=True, editable=False, default="")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    message = models.CharField(max_length=255)
    support = models.ForeignKey(Support_query, on_delete = models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.message_id:
            self.message_id = str(uuid.uuid4().int)[:8]
        super(Support_query_message, self).save(*args, **kwargs)
