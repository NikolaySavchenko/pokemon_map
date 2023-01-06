import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Pokemon
from .models import PokemonEntity

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
    with open('db.sqlite3'):
        pokemons_db = Pokemon.objects.all()
        pokemons_on_map = PokemonEntity.objects.filter(disappeared_at__gt=localtime())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons_on_map:
        add_pokemon(
            folium_map, pokemon.latitude,
            pokemon.longitude,
            f'media/{pokemon.pokemon.photo}',
        )

    pokemons_on_mainpage = []
    for pokemon in pokemons_db:
        pokemons_on_mainpage.append({
            'pokemon_id': pokemon.id,
            'img_url': f'media/{pokemon.photo}',
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_mainpage,
    })


def show_pokemon(request, pokemon_id):
    with open('db.sqlite3'):
        pokemon_db = Pokemon.objects.get(id=int(pokemon_id))
        pokemons_on_map = PokemonEntity.objects.filter(pokemon=pokemon_db,
                                                       disappeared_at__gt=localtime())

    if pokemon_db:
        requested_pokemon = {
            'pokemon_id': pokemon_db.id,
            'img_url': f'../../media/{pokemon_db.photo}',
            'title_ru': pokemon_db.title_ru,
            'title_en': pokemon_db.title_en,
            'title_jp': pokemon_db.title_jp,
            'description': pokemon_db.description,
        }
        if pokemon_db.next_evolution:
            requested_pokemon['next_evolution'] = {'pokemon_id': pokemon_db.next_evolution.id,
                                                   'img_url': f'../../media/{pokemon_db.next_evolution.photo}',
                                                   'title_ru': pokemon_db.next_evolution.title_ru}
        if pokemon_db.previous_evolution:
            requested_pokemon['previous_evolution'] = {'pokemon_id': pokemon_db.previous_evolution.id,
                                                       'img_url': f'../../media/{pokemon_db.previous_evolution.photo}',
                                                       'title_ru': pokemon_db.previous_evolution.title_ru}
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_on_map:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            f'media/{pokemon_entity.pokemon.photo}',
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
