from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import CarBrand, CarModel, Profile, Review, SparePart, SparePartCategory


class CarBrandAdmin(admin.ModelAdmin):
    list_display = ("id", "brand")
    list_display_links = ("brand",)
    search_fields = ("brand",)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "model_name", "brand_id")
    list_display_links = ("model_name",)
    search_fields = ("model_name",)


class SparePartCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)


class SparePartAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "number", "category")
    list_display_links = ("name", "brand")
    search_fields = ("name", "brand", "number")
    list_filter = ("category",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "spare_part", "mileage", "car_brand", "car_model", "rating", "owner")
    list_display_links = ("spare_part",)
    list_filter = ("rating",)
    # autocomplete_fields = ('spare_part', 'owner')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "drive2_link")
    list_display_links = ("user", "drive2_link")


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профили"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(SparePart, SparePartAdmin)
admin.site.register(SparePartCategory, SparePartCategoryAdmin)
admin.site.register(CarBrand, CarBrandAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Profile, ProfileAdmin)
