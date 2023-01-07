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
    pokemons = Pokemon.objects.all()
    pokemons_for_catch = PokemonEntity.objects.filter(disappeared_at__gt=localtime())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons_for_catch:
        add_pokemon(
            folium_map, pokemon.latitude,
            pokemon.longitude,
            f'media/{pokemon.pokemon.photo}',
        )

    pokemons_on_mainpage = []
    for pokemon in pokemons:
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
    pokemon = Pokemon.objects.get(id=int(pokemon_id))
    pokemons_for_catch = PokemonEntity.objects.filter(pokemon=pokemon,
                                                       disappeared_at__gt=localtime())

    if pokemon:
        requested_pokemon = {
            'pokemon_id': pokemon.id,
            'img_url': f'../../media/{pokemon.photo}',
            'title_ru': pokemon.title_ru,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_jp,
            'description': pokemon.description,
        }

        if pokemon.previous_evolution:
            requested_pokemon['previous_evolution'] = {'pokemon_id': pokemon.previous_evolution.id,
                                                       'img_url': f'../../media/{pokemon.previous_evolution.photo}',
                                                       'title_ru': pokemon.previous_evolution.title_ru}
        if pokemon.next_evolution.first():
            requested_pokemon['next_evolution'] = {'pokemon_id': pokemon.next_evolution.first().id,
                                                   'img_url': f'../../media/{pokemon.next_evolution.first().photo}',
                                                   'title_ru': pokemon.next_evolution.first().title_ru}


    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_for_catch:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            f'media/{pokemon_entity.pokemon.photo}',
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })
