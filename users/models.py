from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin # <-- NEW

#class User(AbstractBaseUser, PermissionsMixin):       # <-- CHANGED
class User(models.Model):    
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]
    firebase_uid = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    profile_image = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

   # is_active = models.BooleanField(default=True)   # <-- NEW
    #is_staff = models.BooleanField(default=False)   # <-- NEW

    #USERNAME_FIELD = "firebase_uid"                 # <-- NEW
    #REQUIRED_FIELDS = []                            # <-- NEW

    def __str__(self):
        return self.firebase_uid
    
class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )

    # Temporary until Developer 2 creates the Listing model
    listing_id = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "listing_id")

    def __str__(self):
        return f"{self.user.firebase_uid} - {self.listing_id}"    
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")

    # temporary until Dev 2 gives Listing model
    listing_id = models.IntegerField()

    rating = models.IntegerField()  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.firebase_uid} - {self.rating}"