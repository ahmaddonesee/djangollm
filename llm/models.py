from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.conf import settings



class UploadFile(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True,null=True)
    text=models.TextField(blank=True,null=True,)
    file=models.FileField(upload_to='uploads/',
        validators=[FileExtensionValidator( allowed_extensions=['txt', 'pdf', 'docx','txt.txt'])])
    uploat_at=models.DateTimeField(auto_now_add=True)
    elidt_at=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    


class Comment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    uploadfile=models.ForeignKey(UploadFile,on_delete=models.CASCADE)
    text=models.CharField(max_length=300,blank=True,null=True)
    uploat_at=models.DateTimeField(auto_now_add=True)
    elidt_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user