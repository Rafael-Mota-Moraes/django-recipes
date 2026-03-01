from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeAPIv2TestMixin:
    def get_recipe_raw_data(self):
        return {
            "title": "This is the title",
            "description": "this is the description",
            "preparation_time": 1,
            "preparation_time_unit": "minutes",
            "servings": 1,
            "servings_unit": "Person",
            "preparation_steps": "The preparation steps",
        }

    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse("recipes:recipes-api-list")
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response

    def get_auth_data(self, username="user", password="password"):
        userdata = {"username": username, "password": password}
        user = self.make_author(
            username=userdata.get("username"), password=userdata.get("password")
        )
        response = self.client.post(
            reverse("recipes:token_obtain_pair"), data={**userdata}
        )
        return {
            "jwt_access_token": response.data.get("access"),
            "jwt_refresh_token": response.data.get("refresh"),
            "user": user,
        }


class RecipeAPIv2Test(test.APITestCase, RecipeMixin, RecipeAPIv2TestMixin):
    @patch("recipes.views.api.RecipePagination.page_size", 7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)
        response = self.get_recipe_api_list()
        qtd_recipes_received = len(response.data.get("results"))
        self.assertEqual(wanted_number_of_recipes, qtd_recipes_received)

    def test_recipe_api_list_return_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, 200)

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(len(response.data.get("results")), 1)

    @patch("recipes.views.api.RecipePagination.page_size", 10)
    def test_recipe_api_list_can_loads_recipes_by_category_id(self):
        category_wanted = self.make_category(name="WANTED_CATEGORY")
        category_not_wanted = self.make_category(name="NOT_WANTED_CATEGORY")
        recipes = self.make_recipe_in_batch(qtd=10)

        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        recipes[0].category = category_not_wanted
        recipes[0].save()

        api_url = (
            reverse("recipes:recipes-api-list") + f"?category_id={category_wanted.id}"
        )
        response = self.get_recipe_api_list(api_url)
        self.assertEqual(len(response.data.get("results")), 9)

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(response.status_code, 401)

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        access_token = auth_data.get("jwt_access_token")

        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username="test_patch")
        recipe.author = access_data.get("user")
        access_token = access_data.get("jwt_access_token")
        recipe.save()
        author = access_data.get("user")

        wanted_new_title = f"the new title updated by {author.username}"

        response = self.client.patch(
            reverse("recipes:recipes-api-detail", args=(recipe.id,)),
            data={"title": wanted_new_title},
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        self.assertEqual(response.data.get("title"), wanted_new_title)
