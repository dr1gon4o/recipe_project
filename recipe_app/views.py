from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Recipe, Chef, Post
from .forms import RecipeForm, ChefForm, PostForm
from django.shortcuts import redirect


# Home View - Lists all recipes on the landing page
class HomeView(ListView):
    model = Recipe
    template_name = 'home.html'
    context_object_name = 'recipes'
    # paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()  # Add posts to the context
        return context


class CreateChefProfileView(LoginRequiredMixin, CreateView):
    model = Chef
    form_class = ChefForm
    template_name = 'create_chef_profile.html'
    # success_url = reverse_lazy('profile')

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
            form.instance.user = self.request.user.chef  # Link the new Chef profile to the user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')


class ProfileView(DetailView):
    model = Chef
    template_name = 'profile.html'
    context_object_name = 'chef'

    def get_object(self):
        # Return the Chef profile of the logged-in user, or raise a 404 if it doesn't exist
        try:
            return self.request.user.chef
        except Chef.DoesNotExist:
            return redirect('create_chef_profile')


    # def get_object(self):
    #     return self.request.user.chef  # Fetch the Chef profile for the logged-in user


class ProfileUpdateView(UpdateView):
    model = Chef
    form_class = ChefForm
    template_name = 'update_profile.html'
    context_object_name = 'chef'
    # success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.chef  # Get the Chef instance linked to the logged-in user

    def get_success_url(self):
        return reverse_lazy('profile')  # Redirect to the profile view after successful update


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, f"Account created for {form.cleaned_data['username']}!")
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = 'login.html'
    # success_url = reverse_lazy('profile')

    def get_success_url(self):
        return reverse_lazy('profile')


class LogoutUserView(LogoutView):
    next_page = '/'  # Redirect to home after logout
    # success_url = reverse_lazy('logout')
    # def get_success_url(self):
    #     return reverse_lazy('logout')
    # def get_success_url(self):
    #     return reverse_lazy('home')


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'create_recipe.html'

    def form_valid(self, form):

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
        return reverse_lazy('home')  # Redirect to home after successful recipe creation
        # return reverse_lazy('view_recipe', kwargs={'pk': self.object.pk})


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'update_recipe.html'
    # success_url = reverse_lazy('home')

    # def get_queryset(self):
    #     # return Recipe.objects.filter(chef=self.request.user)  # Only allow deleting recipes created by the logged-in user
    #     queryset = Recipe.objects.filter(chef=self.request.user)
    #     if not queryset.exists():
    #         raise PermissionDenied("You do not have permission to edit or delete this recipe.")
    #     return queryset

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        # form.save_m2m()  # Save many-to-many relationships (categories, ingredients)
        messages.success(self.request, 'Recipe updated successfully!')
        return response

    def get_success_url(self):
        return reverse_lazy('home')  # Redirect to home after successful update
        # return reverse_lazy('view_recipe', kwargs={'pk': self.object.pk})


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'delete_recipe.html'
    context_object_name = 'recipe'
    # success_url = reverse_lazy('home')

    # def get_queryset(self):
    #     # return Recipe.objects.filter(chef=self.request.user)  # Only allow deleting recipes created by the logged-in user
    #     queryset = Recipe.objects.filter(chef=self.request.user)
    #     if not queryset.exists():
    #         raise PermissionDenied("You do not have permission to edit or delete this recipe.")
    #     return queryset

    def get_success_url(self):
        messages.success(self.request, 'Recipe deleted successfully!')
        return reverse_lazy('home')  # Redirect to home after successful deletion


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'view_recipe.html'
    context_object_name = 'recipe'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    context_object_name = 'post'

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
    form_class = PostForm
    template_name = 'update_post.html'
    context_object_name = 'post'


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


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


# no connection to chef model or post or recipe
# class ChefView(DetailView):
#     model = Chef
#     template_name = 'view_chef.html'