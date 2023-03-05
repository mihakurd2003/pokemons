from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemon', null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    Lat = models.FloatField()
    Lot = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
