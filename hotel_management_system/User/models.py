from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
import re

class User(AbstractUser):
    # Fields
    phone_number = models.CharField(max_length=10, blank=True, null=True, unique=True)
    is_hotel_owner = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
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
        full_name = f"{self.first_name} {self.last_name}".strip()
        if not full_name:
            return self.username
        return full_name

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
        return self.hotels.all()

    def get_total_hotels(self):
        """
        Returns the total number of hotels the user owns.
        """
        return self.hotels.count()
    
    def clean(self):
        """Validations to ensure data consistency."""
        super().clean()

        # Ensure phone number is exactly 10 digits if provided
        if self.phone_number and not re.match(r'^\d{10}$', self.phone_number):
            raise ValidationError({'phone_number': "Phone number must be 10 digits."})

        # Prevent a user from being both a hotel owner and a customer
        if self.is_hotel_owner and self.is_customer:
            raise ValidationError("A user cannot be both a hotel owner and a customer at the same time.")

    def save(self, *args, **kwargs):
        """
        Override save method to enforce business rules.
        Automatically assign users to their respective groups based on their role.
        """
        super().save(*args, **kwargs)

        if self.is_hotel_owner:
            group, _ = Group.objects.get_or_create(name='hotel_owner')
            self.groups.add(group)
        elif self.is_customer:
            group, _ = Group.objects.get_or_create(name='customer')
            self.groups.add(group)