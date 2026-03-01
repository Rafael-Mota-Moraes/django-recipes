from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register("recipes/api/v2", views.RecipeAPIv2ViewSet)

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
    path(
        "recipes/api/v2/tag/<int:pk>",
        views.tag_api_detail,
        name="recipe-api-v2-tag",
    ),
    path("recipes/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "recipes/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("recipes/api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(recipe_api_v2_router.urls)),
]
