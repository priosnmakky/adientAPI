from django.db import models
from datetime import datetime, timedelta


class File(models.Model):

    file_no = models.CharField(max_length=150,blank=True, null=True,default='')
    file_name = models.CharField(max_length=150,blank=True, null=True)
    file_size = models.CharField(max_length=150,blank=True, null=True)
    order_count = models.IntegerField(blank=True,null=True)
    status = models.IntegerField(blank=True, null=True)
    customer_id = models.CharField(max_length=50,default='',blank=False, null=False)
    project_id = models.CharField(max_length=50,default='',blank=False, null=False)
    created_by = models.CharField(max_length=15,default='',blank=False, null=False)
    created_date = models.DateTimeField(default=datetime.now(), blank=False)
    updated_by = models.CharField(max_length=150,blank=True, null=True)
    updated_date = models.DateTimeField(default=datetime.now(), blank=True)
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name