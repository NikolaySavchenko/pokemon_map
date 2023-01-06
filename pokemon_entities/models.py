from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(verbose_name='Название рус.', max_length=200)
    title_en = models.CharField(verbose_name='Название eng.', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Название японск.', max_length=200, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    photo = models.ImageField(upload_to='images', verbose_name='Фото', blank=True, null=True)
    next_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Следующая эволюция',
                                       related_name='following_evolution', blank=True, null=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Предыдущая эволюция',
                                           related_name='early_evolution', blank=True, null=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)
    latitude = models.FloatField('Ширина:')
    longitude = models.FloatField('Долгота:')
    appeared_at = models.DateTimeField('Появился в:')
    disappeared_at = models.DateTimeField('Исчезнет в:')
    level = models.IntegerField('Уровень:')
    health = models.IntegerField('Здоровье:')
    strength = models.IntegerField('Сила:')
    defence = models.IntegerField('Защита:')
    stamina = models.IntegerField('Выносливость:')

    def __str__(self):
        return self.pokemon.title_ru
