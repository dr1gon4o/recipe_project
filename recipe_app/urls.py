# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('recipe/create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='update_recipe'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='delete_recipe'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='view_recipe'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),  # New update profile path
]
