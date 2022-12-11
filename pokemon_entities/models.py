from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.title
