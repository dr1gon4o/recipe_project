from django.contrib import admin
from .models import Recipe, Chef, Category, Ingredient

# Custom Admin for the Recipe model
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'chef')

    list_filter = ('chef', 'categories')

    search_fields = ('title', 'description')


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
