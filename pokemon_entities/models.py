from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100, default='title en')
    title_jp = models.CharField(max_length=100, default='title jp')
    image = models.ImageField(upload_to='pokemon', null=True, blank=True)
    description = models.TextField()
    evolution_from = models.ForeignKey('self', on_delete=models.CASCADE, related_name='evolution_to', null=True, blank=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()

    def __str__(self):
        return f'Pokemon entity of {self.pokemon.title_ru}'
