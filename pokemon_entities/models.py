from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='images', blank=True, null=True)
    next_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                       related_name='following_evolution', blank=True, null=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                           related_name='early_evolution', blank=True, null=True)

    def __str__(self):
        return self.title_ru


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

    def __str__(self):
        return self.pokemon
