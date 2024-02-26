from django.db import models


class Employee(models.Model):
    empl_id = models.IntegerField()
    fname = models.CharField(max_length =45 )
    lanme =  models.CharField(max_length =45 )
    salary = models.IntegerField()
    address = models.TextField()
