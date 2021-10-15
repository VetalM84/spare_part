from django.contrib import admin

from .models import SparePart, Car, Mileage, Profile


class SparePartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'number')
    list_display_links = ('id', 'name', 'brand', 'number')
    search_fields = ('name', 'brand', 'number')
    list_filter = ('name', 'brand')


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model_name', 'model_variant')
    list_display_links = ('id', 'brand', 'model_name')
    search_fields = ('brand', 'model_name', 'model_variant')
    list_filter = ('brand', 'model_name')


class MileageAdmin(admin.ModelAdmin):
    list_display = ('id', 'spare_part', 'car', 'mileage', 'owner')
    list_display_links = ('id', 'spare_part', 'car', 'owner')
    search_fields = ('spare_part', 'car')
    list_filter = ('spare_part', 'car')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'drive2_link')
    list_display_links = ('id', 'user', 'drive2_link')
    search_fields = ('user', 'cars')
    list_filter = ('cars',)


admin.site.register(SparePart, SparePartAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Mileage, MileageAdmin)
admin.site.register(Profile, ProfileAdmin)
