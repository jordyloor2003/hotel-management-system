from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_hotel_owner = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )

    # Metadata
    class Meta:
        ordering = ['username']
        verbose_name = "User"
        verbose_name_plural = "Users"

    # Methods
    def __str__(self):
        """
        Returns a readable representation of the user.
        """
        return self.username

    def get_full_name(self):
        """
        Returns the user's full name.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def has_bookings(self):
        """
        Returns True if the user has any bookings.
        """
        return self.bookings.exists()

    def get_total_bookings(self):
        """
        Returns the total number of bookings the user has made.
        """
        return self.bookings.count()

    def is_active_customer(self):
        """
        Returns True if the user is a customer and has active bookings.
        """
        return self.is_customer and self.bookings.filter(status='confirmed').exists()

    def get_hotels_owned(self):
        """
        Returns a list of hotels owned by the user (if they are a hotel owner).
        """
        if self.is_hotel_owner:
            return self.hotels.all()
        return []

    def get_total_hotels(self):
        """
        Returns the total number of hotels the user owns.
        """
        return self.hotels.count() if self.is_hotel_owner else 0