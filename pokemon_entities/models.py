from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField('Lat:')
    longitude = models.FloatField('Lon:')
    appeared_at = models.DateTimeField('Appeared at:')
    disappeared_at = models.DateTimeField('Disappeared at:')
    level = models.IntegerField('Level:')
    health = models.IntegerField('Health:')
    strength = models.IntegerField('Strength:')
    defence = models.IntegerField('Defence:')
    stamina = models.IntegerField('Stamina:')

