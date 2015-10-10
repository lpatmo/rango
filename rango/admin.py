from django.contrib import admin
from rango.models import Category, Page

# Register your models here.

#add in this class to customize the admin interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)

