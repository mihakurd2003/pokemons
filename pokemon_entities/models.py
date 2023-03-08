from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Покемон"""
    title_ru = models.CharField('Название(рус)', max_length=100)
    title_en = models.CharField('Название(англ)', max_length=100)
    title_jp = models.CharField('Название(яп)', max_length=100)
    image = models.ImageField('Картинка', upload_to='pokemon', null=True, blank=True)
    description = models.TextField('Описание')
    evolution_from = models.ForeignKey(
        verbose_name='Эволюция(из кого)',
        to='self', on_delete=models.CASCADE,
        related_name='evolution_to',
        null=True, blank=True,
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """Объект покемона"""
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    pokemon = models.ForeignKey(verbose_name='Покемон', to=Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField('Появился')
    disappeared_at = models.DateTimeField('Исчез')
    level = models.IntegerField('Уровень')
    health = models.IntegerField('Здоровье')
    strength = models.IntegerField('Сила')
    defence = models.IntegerField('Защита')
    stamina = models.IntegerField('Выносливость')

    def __str__(self):
        return f'Pokemon entity of {self.pokemon.title_ru}'
