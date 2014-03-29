from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ad(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    ethnicity = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    ad = models.CharField(max_length=512)
    date = models.DateTimeField()
    website = models.ForeignKey(Website)

    def __str__(self):
        return self.name
