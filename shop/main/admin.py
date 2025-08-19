from django.contrib import admin
from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug'] # Какие параметры будут отображаться в админке
    prepopulated_fields = {'slug': ('name',)} # Автоматически заполняем поля для slug

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available'] # Какие параметры в админке мы сможем менять
    prepopulated_fields = {'slug': ('name',)}

