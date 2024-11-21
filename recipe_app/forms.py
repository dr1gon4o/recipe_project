from django import forms
from django.contrib.auth.models import User
# from .models import Chef, Category, Ingredient, Recipe, Post
from .models import Chef, Recipe, Post


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user


class ChefForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = ['name', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


class RecipeForm(forms.ModelForm):
    categories = forms.CharField(max_length=255, required=True, help_text="Enter the categories, separated by commas.")
    ingredients = forms.CharField(max_length=255, required=True,
                                  help_text="Enter the ingredients, separated by commas.")

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'categories', 'ingredients']

    def clean_categories(self):
        data = self.cleaned_data['categories']
        return [category.strip() for category in data.split(',')]  # Split input into a list of categories

    def clean_ingredients(self):
        data = self.cleaned_data['ingredients']
        return [ingredient.strip() for ingredient in data.split(',')]  # Split input into a list of ingredients

    # # Allow the user to enter a custom category and ingredient
    # new_category = forms.CharField(max_length=100, required=False, label='New Category',
    #                                help_text='Enter a new category if needed')
    # new_ingredient = forms.CharField(max_length=100, required=False, label='New Ingredient',
    #                                  help_text='Enter a new ingredient if needed')
    #
    # class Meta:
    #     model = Recipe
    #     fields = ['title', 'instructions', 'categories', 'ingredients']
    #     widgets = {
    #         'instructions': forms.Textarea(attrs={'rows': 6, 'cols': 50}),
    #     }
    #
    # # Custom validation for categories and ingredients
    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     categories = cleaned_data.get('categories')
    #     ingredients = cleaned_data.get('ingredients')
    #     new_category = cleaned_data.get('new_category')
    #     new_ingredient = cleaned_data.get('new_ingredient')
    #
    #     # Ensure at least one category is provided (either selected or custom)
    #     if not categories and not new_category:
    #         raise forms.ValidationError('At least one category must be selected or entered.')
    #
    #     # Ensure at least one ingredient is provided (either selected or custom)
    #     if not ingredients and not new_ingredient:
    #         raise forms.ValidationError('At least one ingredient must be selected or entered.')
    #
    #     return cleaned_data
    #
    # def save(self, commit=True):
    #     # First, save the Recipe instance
    #     recipe = super().save(commit=False)
    #
    #     # If the new category is provided, create it and associate it with the recipe
    #     new_category = self.cleaned_data.get('new_category')
    #     if new_category:
    #         category, created = Category.objects.get_or_create(name=new_category)
    #         recipe.categories.add(category)
    #
    #     # If the new ingredient is provided, create it and associate it with the recipe
    #     new_ingredient = self.cleaned_data.get('new_ingredient')
    #     if new_ingredient:
    #         ingredient, created = Ingredient.objects.get_or_create(name=new_ingredient)
    #         recipe.ingredients.add(ingredient)
    #
    #     # Add selected categories and ingredients to the recipe
    #     categories = self.cleaned_data.get('categories')
    #     ingredients = self.cleaned_data.get('ingredients')
    #
    #     if categories:
    #         recipe.categories.add(*categories)
    #     if ingredients:
    #         recipe.ingredients.add(*ingredients)
    #
    #     if commit:
    #         recipe.save()
    #
    #     return recipe


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['recipe', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'cols': 50}),
        }
