from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
from django.db.models import Q
from recipes.utils import make_recipe
from recipes.models import Recipe


def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', {
        'recipes': recipes
    })


def category(request: HttpRequest, category_id) -> HttpResponse:
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/category.html', {
        'recipes': recipes,
        'title': f'{recipes[0].category.name}'  # type: ignore
    })


def recipe(request: HttpRequest, id: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe.objects.filter(pk=id, is_published=True))

    return render(request, 'recipes/pages/recipe-view.html', {
        'recipe': recipe,
        'is_detail_page': True
    })


def search(request: HttpRequest) -> HttpResponse:
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(Q(title__icontains=search_term) |
          Q(description__icontains=search_term)),
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for {search_term}',
        'search_term': search_term,
        'recipes': recipes,
    })
