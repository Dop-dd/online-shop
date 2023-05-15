from django.contrib import admin

# Register your models here.
from . models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # pre-populate the fields
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # pre-populate the fields
    prepopulated_fields = {'slug': ('title',)}
