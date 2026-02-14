from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
from django.db.models import Q
from recipes.models import Recipe
from django.core.paginator import Paginator
from utils.pagination import make_pagination
import os
from django.contrib import messages
PER_PAGES = os.environ.get('PER_PAGE', 6)


def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGES
    )

    messages.success(request, 'aoooo')

    return render(request, 'recipes/pages/home.html', {
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request: HttpRequest, category_id) -> HttpResponse:
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))
    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGES
    )
    return render(request, 'recipes/pages/category.html', {
        'recipes': page_obj,
        'pagination_range': pagination_range,
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

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGES
    )

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for {search_term}',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'aditional_url_query': f'&q={search_term}',
    })
