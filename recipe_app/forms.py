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


# class RecipeForm(forms.ModelForm):
#     # Free text input for categories and ingredients (no pre-selection of existing ones)
#     categories = forms.CharField(
#         max_length=255,
#         required=False,
#         help_text="Enter new categories, separated by commas."
#     )
#     ingredients = forms.CharField(
#         max_length=255,
#         required=False,
#         help_text="Enter new ingredients, separated by commas."
#     )
#
#     class Meta:
#         model = Recipe
#         fields = ['title', 'description', 'instructions', 'categories', 'ingredients']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter recipe description'}),
#             'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter cooking instructions'}),
#         }
#
#     # def __init__(self, *args, **kwargs):
#     #     super(RecipeForm, self).__init__(*args, **kwargs)
#     #
#     #     # Prefill categories and ingredients for updates
#     #     if self.instance.pk:  # This means we are updating an existing recipe
#     #         category_names = ', '.join([category.name for category in self.instance.categories.all()])
#     #         ingredient_names = ', '.join([ingredient.name for ingredient in self.instance.ingredients.all()])
#     #         self.fields['categories'].initial = category_names
#     #         self.fields['ingredients'].initial = ingredient_names
#
#     def clean_categories(self):
#         data = self.cleaned_data['categories']
#         category_names = [category.strip() for category in data.split(',')]  # Split categories by commas
#         # Create new categories if they don't exist
#         categories = []
#         for category_name in category_names:
#             category_obj, created = Category.objects.get_or_create(name=category_name)
#             categories.append(category_obj)
#         return categories
#
#     def clean_ingredients(self):
#         data = self.cleaned_data['ingredients']
#         ingredient_names = data.split(',')  # Split ingredients by commas
#         # Create new ingredients if they don't exist
#         ingredients = []
#         for ingredient_name in ingredient_names:
#             ingredient_obj, created = Ingredient.objects.get_or_create(name=ingredient_name)
#             ingredients.append(ingredient_obj)
#         return ingredients
#
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#
#         if commit:
#             instance.save()
#
#         # Save the categories and ingredients relationships (many-to-many fields)
#         instance.categories.set(self.cleaned_data['categories'])
#         instance.ingredients.set(self.cleaned_data['ingredients'])
#
#         return instance


class RecipeForm(forms.ModelForm):
    categories = forms.CharField(max_length=255, required=True,
                                 help_text="Enter the categories, separated by commas.",
                                 widget=forms.TextInput(attrs={'placeholder': 'e.g., lunch, dinner'}),)
    ingredients = forms.CharField(max_length=255, required=True,
                                  help_text="Enter the ingredients, separated by commas.",
                                  widget=forms.TextInput(attrs={'placeholder': 'e.g., sugar, flour'}),)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'categories', 'ingredients']
        widgets = {
                    'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title'}),
                    'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter recipe description'}),
                    'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter cooking instructions'}),
                }

    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # If the form is bound to an instance (update scenario), populate the fields
        if self.instance.pk:  # Check if an instance is passed (update form)
            self.fields['categories'].initial = ', '.join([c.name for c in self.instance.categories.all()])
            self.fields['ingredients'].initial = ', '.join([i.name for i in self.instance.ingredients.all()])


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

    def save(self, commit=True):
        # Override save method to handle many-to-many relationships
        instance = super().save(commit=False)

        if commit:
            instance.save()  # Save the instance to generate a primary key if necessary
            # Add categories and ingredients
            instance.categories.set(self.cleaned_data['categories'])
            instance.ingredients.set(self.cleaned_data['ingredients'])

        return instance


class RecipeEditForm(RecipeForm):
    class Meta(RecipeForm.Meta):
        model = Recipe
        exclude = ['categories', 'ingredients']


# class RecipeDeleteForm(RecipeForm):
#     pass


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['recipe', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter recipe comment'}),
        }


class PostEditForm(PostForm):
    class Meta(PostForm.Meta):
        exclude = ['recipe']


# class PostDeleteForm(PostForm):
#     pass
