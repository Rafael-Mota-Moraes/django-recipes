from typing import Any

from recipes.models import Recipe
from django import forms
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self._errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_preparation_time()
        self.clean_servings()

        cd = self.data

        title: str = cd.get("title", "")
        description: str = cd.get("description", "")

        if len(title) < 5:
            self._errors["title"].append("Title must have at least 5 chars.")

        if title == description:
            self._errors["title"].append(
                "Title and description are equal, this is not allowed"
            )
            self._errors["description"].append(
                "Title and description are equal, this is not allowed"
            )
        if self._errors:
            raise self.ErrorClass(self._errors)  # type: ignore

    def clean_preparation_time(self):
        field_name = "preparation_time"
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self._errors[field_name].append("Must be a positive number")

        return field_value

    def clean_servings(self):
        field_name = "servings"
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self._errors[field_name].append("Must be a positive number")

        return field_value
