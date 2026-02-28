from django.urls import path
from . import views
from .views import site

app_name = "recipes"

urlpatterns = [
    path("", views.RecipeListViewHome.as_view(), name="home"),
    path(
        "recipes/tags/<slug:slug>", views.RecipeListViewTag.as_view(), name="tag"
    ),  # type: ignore
    path(
        "recipes/search/", views.RecipeListViewSearch.as_view(), name="search"
    ),  # type: ignore
    path(
        "recipes/category/<int:category_id>/",
        views.RecipeListViewCategory.as_view(),
        name="category",
    ),
    path("recipes/<int:pk>/", views.RecipeDetail.as_view(), name="recipe"),
    path(
        "recipes/api/v1/", views.RecipeListViewHomeApi.as_view(), name="recipes_api_v1"
    ),
    path(
        "recipes/api/v1/<int:pk>",
        views.RecipeDetailApiV1.as_view(),
        name="recipe_detail_api_v1",
    ),
    path("recipes/theory", views.theory, name="theory"),
    path("recipes/api/v2/", views.recipe_api_list, name="recipe-api-v2"),
    path(
        "recipes/api/v2/<int:pk>", views.recipe_api_detail, name="recipe-api-v2-detail"
    ),
    path(
        "recipes/api/v2/tag/<int:pk>",
        views.tap_api_detail,
        name="recipe-api-v2-tag",
    ),
]
