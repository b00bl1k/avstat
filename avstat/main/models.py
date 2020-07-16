from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)


class Stat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField()
    total = models.IntegerField()
    added = models.IntegerField()

    class Meta:
        unique_together = ['user', 'created_at']
