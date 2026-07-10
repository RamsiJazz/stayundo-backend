# users/admin.py

from django.contrib import admin
from .models import User, Wishlist, Review


class UserAdmin(admin.ModelAdmin):
    list_display = ('firebase_uid', 'role', 'name', 'email')


admin.site.register(User, UserAdmin)
admin.site.register(Wishlist)
admin.site.register(Review)