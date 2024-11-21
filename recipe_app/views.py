from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Recipe, Chef  # Ensure Chef is imported correctly
from .forms import RecipeForm, ChefForm

# Home View - Lists all recipes on the landing page
class HomeView(ListView):
    model = Recipe
    template_name = 'home.html'
    context_object_name = 'recipes'

# Profile View - to show the user's profile page
class ProfileView(DetailView):
    model = Chef
    template_name = 'profile.html'
    context_object_name = 'chef'

    def get_object(self):
        return self.request.user.chef  # Fetch the Chef profile for the logged-in user

# Profile Update View - to allow the user to edit their profile
class ProfileUpdateView(UpdateView):
    model = Chef
    form_class = ChefForm
    template_name = 'update_profile.html'

    def get_object(self):
        return self.request.user.chef  # Get the Chef instance linked to the logged-in user

    def get_success_url(self):
        return reverse_lazy('profile')  # Redirect to the profile view after successful update

# User Registration (Create user using CBV)
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, f"Account created for {form.cleaned_data['username']}!")
        return super().form_valid(form)

# User Login (Using Django's built-in LoginView)
class LoginUserView(LoginView):
    template_name = 'login.html'

# User Logout (Using Django's built-in LogoutView)
class LogoutUserView(LogoutView):
    next_page = '/'  # Redirect to home after logout

# Recipe Create (Create a new recipe with CBV)
class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'create_recipe.html'

    def form_valid(self, form):
        form.instance.chef = self.request.user  # Set the logged-in user as the chef
        response = super().form_valid(form)
        form.save_m2m()  # Save the many-to-many relationships (categories, ingredients)
        messages.success(self.request, 'Recipe created successfully!')
        return response

    def get_success_url(self):
        # return reverse_lazy('home')  # Redirect to home after successful recipe creation
        return reverse_lazy('view_recipe', kwargs={'pk': self.object.pk})

# Recipe Update (Update an existing recipe with CBV)
class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'update_recipe.html'

    def get_queryset(self):
        # return Recipe.objects.filter(chef=self.request.user)  # Only allow deleting recipes created by the logged-in user
        queryset = Recipe.objects.filter(chef=self.request.user)
        if not queryset.exists():
            raise PermissionDenied("You do not have permission to edit or delete this recipe.")
        return queryset

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save_m2m()  # Save many-to-many relationships (categories, ingredients)
        messages.success(self.request, 'Recipe updated successfully!')
        return response

    def get_success_url(self):
        # return reverse_lazy('home')  # Redirect to home after successful update
        return reverse_lazy('view_recipe', kwargs={'pk': self.object.pk})

# Recipe Delete (Delete a recipe with CBV)
class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'delete_recipe.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        # return Recipe.objects.filter(chef=self.request.user)  # Only allow deleting recipes created by the logged-in user
        queryset = Recipe.objects.filter(chef=self.request.user)
        if not queryset.exists():
            raise PermissionDenied("You do not have permission to edit or delete this recipe.")
        return queryset

    def get_success_url(self):
        messages.success(self.request, 'Recipe deleted successfully!')
        return reverse_lazy('home')  # Redirect to home after successful deletion

# Recipe Detail (View the details of a single recipe)
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'view_recipe.html'
    context_object_name = 'recipe'
