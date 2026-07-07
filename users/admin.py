# users/admin.py
from django.contrib import admin
from .models import User, Wishlist, Review

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('firebase_uid', 'role', 'name', 'email')
admin.site.register(Wishlist)
admin.site.register(Review)