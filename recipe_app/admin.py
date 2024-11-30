from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Recipe, Chef, Category, Ingredient

# Custom Admin for the Recipe model
class RecipeAdmin(admin.ModelAdmin):
    # 1. List display (which fields to display in the admin list view)
    list_display = ('title', 'chef')  # Display title, chef, created_at, and is_featured

    # 2. List filters (filter options in the sidebar)
    list_filter = ('chef', 'categories')  # Filter by chef, categories, and featured status

    # 3. Search fields (search for records by specific fields)
    search_fields = ('title', 'description')  # Search by title or description


    # 5. Custom Action (bulk action to mark recipes as featured)
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = 'Mark selected recipes as featured'
    actions = [mark_as_featured]  # Add the custom action to the admin panel

# Register Recipe with the custom admin
admin.site.register(Recipe, RecipeAdmin)

# Similarly, you can customize other models (Chef, Category, Ingredient) if needed
admin.site.register(Chef)
admin.site.register(Category)
admin.site.register(Ingredient)
