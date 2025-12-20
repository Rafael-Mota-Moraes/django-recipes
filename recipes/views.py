from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from recipes.utils import make_recipe


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'recipes/pages/home.html', {
        'recipes': [make_recipe() for _ in range(10)]
    })


def recipe(request: HttpRequest, id: int) -> HttpResponse:
    return render(request, 'recipes/pages/recipe-view.html', {
        'recipe': make_recipe(),
        'is_detail_page': True
    })
