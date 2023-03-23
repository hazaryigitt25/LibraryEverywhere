from django.contrib import admin

from .models import Library,Books
# Register your models here.

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    
    list_display = ["lib_name","lib_city"]
    list_display_links = ["lib_name"]
    search_fields = ["lib_name","lib_city"]
    list_filter = ["lib_city"]
    class Meta:
        model = Library
        
@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ["book_name","book_author","lib_name","lib_city"]
    search_fields = ["book_name"]
    list_filter = ["book_author","lib_name"]
    class Meta:
        model = Books
