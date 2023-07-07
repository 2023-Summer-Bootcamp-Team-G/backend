from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    
    class Meta:
        abstract = True
        
class User(BaseModel):
    login_id = models.CharField(max_length=200, null=False, unique=True)
    nick_name = models.CharField(max_length=200, null=False)
    password = models.CharField(max_length=200, null=False)
