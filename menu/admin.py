from django.contrib import admin
from .models import Category, FoodItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'vendor', 'updated_at')
    #as vendor is foreignkey we should search for vendor name inside vendor table
    search_fields = ('category_name', 'vendor__vendor_name')
    prepopulated_fields = {'slug': ('category_name',)}

admin.site.register(Category, CategoryAdmin)

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'is_available', 'price', 'updated_at')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name')
    list_filter = ('is_available', )

admin.site.register(FoodItem, FoodItemAdmin)
