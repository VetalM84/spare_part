from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import SparePart, Mileage, Profile, CarModel, CarBrand, SparePartCategory


class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand')
    list_display_links = ('brand',)
    search_fields = ('brand',)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_name', 'brand_id')
    list_display_links = ('model_name',)
    search_fields = ('model_name',)


class SparePartCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class SparePartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'number', 'category')
    list_display_links = ('id', 'name', 'brand')
    search_fields = ('name', 'brand', 'number')
    list_filter = ('name', 'brand', 'category')


# class CarAdmin(admin.ModelAdmin):
#     list_display = ('id', 'brand', 'model_name', 'generation')
#     list_display_links = ('id', 'brand', 'model_name')
#     search_fields = ('brand', 'model_name', 'generation')
#     list_filter = ('brand', 'model_name')


class MileageAdmin(admin.ModelAdmin):
    list_display = ('id', 'spare_part', 'mileage', 'car_brand', 'car_model', 'rating', 'owner')
    list_display_links = ('id', 'spare_part', 'owner')
    list_filter = ('spare_part', 'rating')
    # autocomplete_fields = ('spare_part', 'owner')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'drive2_link')
    list_display_links = ('id', 'user', 'drive2_link')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(SparePart, SparePartAdmin)
admin.site.register(SparePartCategory, SparePartCategoryAdmin)
# admin.site.register(Car, CarAdmin)
admin.site.register(CarBrand, CarBrandAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Mileage, MileageAdmin)
admin.site.register(Profile, ProfileAdmin)
