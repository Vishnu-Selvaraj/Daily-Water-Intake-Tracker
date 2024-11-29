from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class WaterInke(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateField(default=timezone.now().date())
    time = models.TimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','date')