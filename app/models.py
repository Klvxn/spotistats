from django.db import models


# Create your models here.
class Artist(models.Model):

    artist_id = models.CharField(max_length=15, primary_key=True)
    monthly_listeners = models.CharField(max_length=10)
    stage_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.stage_name} - {self.monthly_listeners}"
