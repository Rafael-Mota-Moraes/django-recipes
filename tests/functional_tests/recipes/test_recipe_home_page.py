from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
from unittest.mock import patch
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGES', new=3)
    def test_recipe_home_page_without_recipes_error_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes published yet.', body.text)

    @patch('recipes.views.PER_PAGES', new=3)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search for a recipe"]')

        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        recipe_found = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'recipe-title'))
        )
        self.assertIn(
            title_needed,
            recipe_found.text,
        )

    @patch('recipes.views.PER_PAGES', new=2)
    def test_recipe_home_page_pagination(self):
        recipes = self.make_recipe_in_batch()

        self.browser.get(self.live_server_url)

        page2 = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Go to page 2"]')
        page2.click()
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)
