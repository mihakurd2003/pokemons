import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    curr_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=curr_time, disappeared_at__gte=curr_time)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else None,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'img_url': requested_pokemon.image.url,
        'description': requested_pokemon.description,
        'entities': [],
    }

    previous_evolution = requested_pokemon.evolution_from
    next_evolution = requested_pokemon.evolution_to.first()

    if previous_evolution:
        pokemon['previous_evolution'] = {
            'title_ru': previous_evolution.title_ru,
            'pokemon_id': previous_evolution.id,
            'img_url': previous_evolution.image.url,
        }
    if next_evolution:
        pokemon['next_evolution'] = {
            'title_ru': next_evolution.title_ru,
            'pokemon_id': next_evolution.id,
            'img_url': next_evolution.image.url,
        }

    pokemon_entities = requested_pokemon.entities.filter(pokemon__id=requested_pokemon.id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
        pokemon['entities'].append({
            'level': pokemon_entity.level,
            'lat': pokemon_entity.lat,
            'lon': pokemon_entity.lon,
        })

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
