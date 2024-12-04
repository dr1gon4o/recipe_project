from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Recipe, Chef, Post, Ingredient, Category
from .forms import RecipeForm, ChefForm, PostForm, PostEditForm, RecipeEditForm, ChefEditForm, UserRegistrationForm
from django.shortcuts import redirect, render, get_object_or_404


class HomeView(ListView):
    model = Recipe
    template_name = 'home.html'
    context_object_name = 'recipes'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Paginate posts
        post_list = Post.objects.all()
        # recipe_list = Recipe.object.all()
        post_paginator = Paginator(post_list, 6)  # Set the number of posts per page
        page_number = self.request.GET.get('post_page')  # Get the page number for posts
        post_page_obj = post_paginator.get_page(page_number)

        # context['posts'] = Post.objects.all()  # Add posts to the context
        context['posts'] = post_page_obj  # Pass paginated posts to the context
        return context


class CreateChefProfileView(LoginRequiredMixin, CreateView):
    model = Chef
    form_class = ChefForm
    template_name = 'create_chef_profile.html'
    success_url = reverse_lazy('profile')

    # def get_object(self):
    #     """
    #     Try to fetch the Chef profile of the current user.
    #     If no Chef profile exists, create a new one.
    #     """
    #     try:
    #         return self.request.user.chef  # Try to get the user's Chef profile
    #     except Chef.DoesNotExist:
    #         return None  # If no Chef profile, return None (will create new in form_valid())

    # def form_valid(self, form):
    #     # If the Chef profile doesn't exist, it will be created
    #     if not self.get_object():
    #         form.instance.user = self.request.user.chef  # Link the new Chef profile to the user
    #     return super().form_valid(form)

    def form_valid(self, form):
        # If the Chef profile doesn't exist, create it
        if not hasattr(self.request.user, 'chef'):
            form.instance.user = self.request.user  # Link the new Chef profile to the user
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('profile')


# class ProfileView(DetailView):
#     model = Chef
#     template_name = 'profile.html'
#     context_object_name = 'chef'
#
#     def get_object(self):
#         # Return the Chef profile of the logged-in user, or raise a 404 if it doesn't exist
#         try:
#             return self.request.user.chef
#         except Chef.DoesNotExist:
#             return redirect('create_chef_profile')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Fetch recipes created by this chef
#         context['recipes'] = Recipe.objects.filter(chef=self.get_object())
#         return context

    # def get_object(self):
    #     return self.request.user.chef  # Fetch the Chef profile for the logged-in user

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # # Check if the user has a Chef profile
        # chef = getattr(self.request.user, 'chef', None)
        # context['chef'] = chef  # Pass Chef object or None to the template
        #
        # # If the user has a Chef, fetch their recipes
        # if chef:
        #     context['recipes'] = Recipe.objects.filter(chef=chef)
        # else:
        #     context['recipes'] = None  # No recipes for users without a Chef profile
        # return context

        # Fetch chef by ID if provided, otherwise default to the logged-in user
        chef_id = self.kwargs.get('chef_id')
        if chef_id:
            chef = get_object_or_404(Chef, id=chef_id)
        else:
            chef = getattr(self.request.user, 'chef', None)

        context['chef'] = chef
        context['recipes'] = Recipe.objects.filter(chef=chef) if chef else None
        return context


class ProfileUpdateView(UpdateView):
    model = Chef
    form_class = ChefEditForm
    template_name = 'update_profile.html'
    context_object_name = 'chef'
    # success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.chef  # Get the Chef instance linked to the logged-in user

    def get_success_url(self):
        return reverse_lazy('profile')  # Redirect to the profile view after successful update


class RegisterView(CreateView):
    # form_class = UserCreationForm
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, f"Account created for {form.cleaned_data['username']}!")
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = 'login.html'
    # success_url = reverse_lazy('profile')

    def get_success_url(self):
        # return reverse_lazy('profile')
        return reverse_lazy('home')


class LogoutUserView(LogoutView):
    next_page = '/'  # Redirect to home after logout
    # template_name = 'logout.html'
    # success_url = reverse_lazy('logout')
    # def get_success_url(self):
    #     return reverse_lazy('logout')
    # def get_success_url(self):
    #     return reverse_lazy('home')


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'create_recipe.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        if not self.request.user.chef:
            messages.error(self.request, "You need to create a Chef profile first.")
            return redirect('create_chef_profile')  # Redirect to the Chef profile creation page
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

    # def get_success_url(self):
    #     return reverse_lazy('home')  # Redirect to home after successful recipe creation
    #     # return reverse_lazy('view_recipe', kwargs={'pk': self.object.pk})


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeEditForm
    template_name = 'update_recipe.html'
    success_url = reverse_lazy('home')
    # success_url = reverse_lazy('view_recipe', kwargs={'pk': self.object.pk})

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

    # def get_success_url(self):
    #     return reverse_lazy('home')  # Redirect to home after successful update
        # return reverse_lazy('view_recipe', kwargs={'pk': self.object.pk})


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'delete_recipe.html'
    context_object_name = 'recipe'
    success_url = reverse_lazy('home')

    # def get_queryset(self):
    #     # return Recipe.objects.filter(chef=self.request.user)  # Only allow deleting recipes created by the logged-in user
    #     queryset = Recipe.objects.filter(chef=self.request.user)
    #     if not queryset.exists():
    #         raise PermissionDenied("You do not have permission to edit or delete this recipe.")
    #     return queryset

    # def get_success_url(self):
    #     messages.success(self.request, 'Recipe deleted successfully!')
    #     return reverse_lazy('home')  # Redirect to home after successful deletion


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'view_recipe.html'
    context_object_name = 'recipe'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Optionally, you can add user-specific behavior, like linking the post to a user or chef
        form.instance.user = self.request.user
        # form.save_m2m()
        form.save()
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('home')  # Redirect to home or a post listing page after creating a post


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'update_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    # def get_success_url(self):
    #     return reverse_lazy('home')  # Redirect to home or a post listing page after updating a post


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    # def get_success_url(self):
    #     return reverse_lazy('home')  # Redirect to home after deleting a post


class PostDetailView(DetailView):
    model = Post
    template_name = 'view_post.html'
    context_object_name = 'post'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe_list.html'
    context_object_name = 'recipes'


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredient_list.html'
    context_object_name = 'ingredients'


def ajax_search(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request

    # Perform the search if query exists
    if query:
        recipe_results = Recipe.objects.filter(title__icontains=query)
        post_results = Post.objects.filter(comment__icontains=query)
        category_results = Category.objects.filter(name__icontains=query)
        ingredient_results = Ingredient.objects.filter(name__icontains=query)

        # Combine the results in a dictionary
        results = {
            'recipes': [recipe.title for recipe in recipe_results],
            'posts': [post.comment for post in post_results],
            'categories': [category.name for category in category_results],
            'ingredients': [ingredient.name for ingredient in ingredient_results],
        }
        return JsonResponse(results)  # Return the results as a JSON response

    return JsonResponse({'error': 'No search query provided.'})


def SearchView(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
        posts = Post.objects.filter(comment__icontains=query)
        categories = Category.objects.filter(name__icontains=query)
        ingredients = Ingredient.objects.filter(name__icontains=query)
    else:
        recipes = posts = categories = ingredients = []

    return render(request, 'search_results.html', {
        'recipes': recipes,
        'posts': posts,
        'categories': categories,
        'ingredients': ingredients,
    })


# class PaginatedRecipesView(View):
#     def get(self, request, *args, **kwargs):
#         # Get all recipes
#         recipe_list = Recipe.objects.all()
#
#         # Pagination setup: 6 recipes per page
#         paginator = Paginator(recipe_list, 6)
#         page_number = request.GET.get('page', 1)  # Default to page 1 if not provided
#         page_obj = paginator.get_page(page_number)
#
#         # Prepare the data to send back
#         recipes_data = [{
#             'id': recipe.id,
#             'title': recipe.title,
#             'description': recipe.description,
#             # 'created_at': recipe.created_at,
#             # 'image_url': recipe.image.url if recipe.image else None,  # Optional image
#         } for recipe in page_obj]
#
#         # Pagination metadata
#         pagination_data = {
#             'current_page': page_obj.number,
#             'total_pages': paginator.num_pages,
#             'has_previous': page_obj.has_previous(),
#             'has_next': page_obj.has_next(),
#             'total_items': paginator.count,
#             'recipes': recipes_data
#         }
#
#         return JsonResponse(pagination_data)


# no connection to chef model or post or recipe
# class ChefView(DetailView):
#     model = Chef
#     template_name = 'view_chef.html'
class ChefProfileView(DetailView):
    model = Chef
    template_name = 'chef_profile.html'
    context_object_name = 'chef'

    def get_object(self):
        # Fetch the Chef based on the provided ID
        chef_id = self.kwargs.get('chef_id')
        return get_object_or_404(Chef, id=chef_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include all recipes created by this chef
        context['recipes'] = Recipe.objects.filter(chef=self.get_object())
        return context
