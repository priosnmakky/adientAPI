from django.db import models

# Create your models here.

class File_order(models.Model):
    item = models.IntegerField(blank=False, null=False)
    customer_code = models.CharField(max_length=150,blank=False, default='')
    customer_description = models.CharField(max_length=250,blank=False, default='')
    project_code = models.CharField(max_length=250,blank=False, default='')
    transporter = models.CharField(max_length=250,blank=False, default='')
    effective_date = models.DateTimeField(default=datetime.now(), blank=True)
    expire_date = models.DateTimeField(default=datetime.now(), blank=True)
