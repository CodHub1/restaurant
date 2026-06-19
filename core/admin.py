"""Регистрация моделей в админ-панели Django."""
from django.contrib import admin

from .models import Booking, Category, Dish, Feedback, News


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    list_editable = ('price', 'is_available')
    search_fields = ('name', 'description')
    autocomplete_fields = ('category',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': ('category', 'name', 'description', 'price', 'image', 'is_available')}),
        ('Служебное', {'fields': ('created_at',)}),
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title', 'content')
    date_hierarchy = 'published_at'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time', 'guests', 'status', 'created_at')
    list_filter = ('status', 'date')
    list_editable = ('status',)
    search_fields = ('name', 'phone')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read',)
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
