from django import forms
from .models import Chef, Category, Ingredient, Recipe, Post


class ChefForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = ['name', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['chef', 'title', 'instructions', 'categories', 'ingredients']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 6, 'cols': 50}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['recipe', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'cols': 50}),
        }
