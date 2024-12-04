from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Chef, Recipe, Post, Category, Ingredient


# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     password_confirm = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta:
#         model = User
#         fields = ['email']  # Only email is required for registration
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")
#
#         if password != password_confirm:
#             raise forms.ValidationError("Passwords do not match.")
#         return cleaned_data
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = user.email  # Use the email as the username
#         if commit:
#             user.set_password(self.cleaned_data['password'])
#             user.save()
#         return user

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].max_length = 50
        self.fields['username'].help_text = "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."


class ChefForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = ['name', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


class ChefEditForm(ChefForm):
    pass


class RecipeForm(forms.ModelForm):
    categories = forms.CharField(max_length=255, required=True, help_text="Enter the categories, separated by commas.")
    ingredients = forms.CharField(max_length=255, required=True, help_text="Enter the ingredients, separated by commas.")

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'categories', 'ingredients']

    def clean_categories(self):
        data = self.cleaned_data['categories']
        categories = [category.strip() for category in data.split(',')]  # Split input into a list of categories
        # Check for duplicates in user input
        if len(categories) != len(set(categories)):
            raise forms.ValidationError("Duplicate categories are not allowed.")
        # Ensure that the categories exist in the database, or create them
        category_objects = []
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            category_objects.append(category)
        return category_objects  # Return the list of Category objects

        # category_objs = []
        # for category in categories:
        #     category_obj, created = Category.objects.get_or_create(name=category)  # Get or create the category
        #     category_objs.append(category_obj)
        # return category_objs

    def clean_ingredients(self):
        data = self.cleaned_data['ingredients']
        ingredients = [ingredient.strip() for ingredient in data.split(',')]  # Split input into a list of ingredients
        # Check for duplicates in user input
        if len(ingredients) != len(set(ingredients)):
            raise forms.ValidationError("Duplicate ingredients are not allowed.")

        # Ensure that the ingredients exist in the database, or create them
        ingredient_objects = []
        for ingredient_name in ingredients:
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
            ingredient_objects.append(ingredient)

        return ingredient_objects  # Return the list of Ingredient objects

        # ingredient_objs = []
        # for ingredient in ingredients:
        #     ingredient_obj, created = Ingredient.objects.get_or_create(name=ingredient)  # Get or create the ingredient
        #     ingredient_objs.append(ingredient_obj)
        # return ingredient_objs


class RecipeEditForm(RecipeForm):
    pass


# class RecipeDeleteForm(RecipeForm):
#     pass


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['recipe', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 6, 'cols': 50}),
        }


class PostEditForm(PostForm):
    class Meta(PostForm.Meta):
        exclude = ['recipe']


# class PostDeleteForm(PostForm):
#     pass
