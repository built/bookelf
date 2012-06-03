from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=512)
    address = models.CharField(max_length=512)

    def __unicode__(self):
        return self.name


class Need(models.Model):
    name = models.CharField(max_length=512)
    details = models.CharField(max_length=512)
    school = models.ForeignKey(School)

    def __unicode__(self):
        return self.name