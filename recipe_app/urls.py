from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),

    path('recipe/create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='update_recipe'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='delete_recipe'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='view_recipe'),

    path('post/create/', views.PostCreateView.as_view(), name='create_post'),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='update_post'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='delete_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='view_post'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='update_profile'),  # New update profile path
    path('profile/create/', views.CreateChefProfileView.as_view(), name='create_chef_profile'),
    # path('profile/create-or-update/', views.CreateOrUpdateChefProfileView.as_view(), name='create_or_update_or_update_chef_profile'),
    # path('chef-profile/', views.CreateOrUpdateChefProfileView.as_view(), name='create_or_update_chef_profile'),  # Create or update the chef profile

    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('ingredients/', views.IngredientListView.as_view(), name='ingredient_list'),

    path('ajax_search/', views.ajax_search, name='ajax_search'),
    # path('recipes/json/', views.PaginatedRecipesView.as_view(), name='recipes_json'),
    path('search/', views.SearchView, name='search'),

    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]