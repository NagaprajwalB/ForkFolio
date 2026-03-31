from django.contrib import admin
from .models import Recipe, Category, Ingredient, Step, Rating

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class StepInline(admin.TabularInline):
    model = Step
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'category']
    search_fields = ['title', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [IngredientInline, StepInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Rating)
