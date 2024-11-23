from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Recipe, Chef, Post  # Ensure Chef is imported correctly
from .forms import RecipeForm, ChefForm, PostForm
from django.shortcuts import redirect
from django.views.generic import DetailView


# Home View - Lists all recipes on the landing page
class HomeView(ListView):
    model = Recipe
    template_name = 'home.html'
    context_object_name = 'recipes'


class CreateOrUpdateChefProfileView(LoginRequiredMixin, CreateView, UpdateView):
    model = Chef
    form_class = ChefForm
    template_name = 'create_or_update_chef_profile.html'

    def get_object(self):
        """
        Try to fetch the Chef profile of the current user.
        If no Chef profile exists, create a new one.
        """
        try:
            return self.request.user.chef  # Try to get the user's Chef profile
        except Chef.DoesNotExist:
            return None  # If no Chef profile, return None (will create new in form_valid())

    def form_valid(self, form):
        # If the Chef profile doesn't exist, it will be created
        if not self.get_object():
            form.instance.user = self.request.user  # Link the new Chef profile to the user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the profile page after creation or update
        return reverse_lazy('profile')


# Profile View - to show the user's profile page
class ProfileView(DetailView):
    model = Chef
    template_name = 'profile.html'
    context_object_name = 'chef'

    def get_object(self):
        # Return the Chef profile of the logged-in user, or raise a 404 if it doesn't exist
        try:
            return self.request.user.chef
        except Chef.DoesNotExist:
            return redirect('create_or_update_chef_profile')

    # def get_object(self):
    #     return self.request.user.chef  # Fetch the Chef profile for the logged-in user

# Profile Update View - to allow the user to edit their profile
class ProfileUpdateView(UpdateView):
    model = Chef
    form_class = ChefForm
    template_name = 'update_profile.html'
    context_object_name = 'chef'

    def get_object(self):
        # return self.request.user.chef  # Get the Chef instance linked to the logged-in user
        return self.request.user  # Get the Chef instance linked to the logged-in user

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
    def get_success_url(self):
        return reverse_lazy('profile')


# User Logout (Using Django's built-in LogoutView)
class LogoutUserView(LogoutView):
    next_page = '/'  # Redirect to home after logout
    # def get_success_url(self):
    #     return reverse_lazy('logout')
    # success_url_allowed_hosts = reverse_lazy('home')
    # template_name = 'logout.html'
    # def get_success_url(self):
    #     return reverse_lazy('home')

# Recipe Create (Create a new recipe with CBV)
class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'create_recipe.html'

    def form_valid(self, form):
        # Check if the user has a Chef profile
        # if not hasattr(self.request.user, 'chef'):  # User doesn't have a Chef profile
        #     messages.error(self.request, "You need to create a Chef profile first.")
        #     return redirect('create_or_update_chef_profile')  # Redirect to the Chef profile creation page
        # Ensure the logged-in user has a Chef profile
        if not self.request.user.chef:
            messages.error(self.request, "You need to create a Chef profile first.")
            return redirect('create_or_update_chef_profile')  # Redirect to the Chef profile creation page
        # Get or create the Chef instance linked to the logged-in user
        chef = self.request.user.chef  # Access the Chef instance associated with the current User
        # Assign the Chef instance to the recipe's chef field
        form.instance.chef = chef
        # Save the recipe form and handle many-to-many relationships
        response = super().form_valid(form)
        # Save the recipe form and get the model instance
        # recipe = form.save()  # Save the form, but don't commit to DB yet
        form.save()
        # Save many-to-many relationships (categories, ingredients)
        # form.save_m2m()  # This is called on the form, not the instance
        # Add a success message
        messages.success(self.request, 'Recipe created successfully!')

        return response

    # def form_valid(self, form):
    #     form.instance.chef = self.request.user  # Set the logged-in user as the chef
    #     response = super().form_valid(form)
    #     form.save_m2m()  # Save the many-to-many relationships (categories, ingredients)
    #     messages.success(self.request, 'Recipe created successfully!')
    #     return response

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
        return reverse_lazy('home')  # Redirect to home after successful update
        # return reverse_lazy('view_recipe', kwargs={'pk': self.object.pk})

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


class PostCreateView(CreateView):
    model = Post
    template_name = 'create_post.html'
    context_object_name = 'post'
    fields = ['recipe', 'comment']  # Adjust fields as needed

    def form_valid(self, form):
        # Optionally, you can add user-specific behavior, like linking the post to a user or chef
        form.instance.user = self.request.user
        # form.save_m2m()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')  # Redirect to home or a post listing page after creating a post

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    context_object_name = 'post'
    fields = ['recipe', 'comment']  # Adjust fields as needed

    def get_success_url(self):
        return reverse_lazy('home')  # Redirect to home or a post listing page after updating a post


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('home')  # Redirect to home after deleting a post

class PostDetailView(DetailView):
    model = Post
    template_name = 'view_post.html'
    context_object_name = 'post'