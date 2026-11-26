
from django.contrib import admin

from .models import LibraryCategory, LibraryVideo


@admin.register(LibraryCategory)
class LibraryCategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "slug", "is_active", "display_order")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(LibraryVideo)
class LibraryVideoAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "duration_seconds",
        "is_published",
        "published_at",
    )
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("category", "is_published")
    search_fields = ("title", "description")
