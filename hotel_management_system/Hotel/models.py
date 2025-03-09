from django.db import models
from User.models import User

class Hotel(models.Model):
    # Fields
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hotels")
    total_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()
    price_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta:
        ordering = ['name']
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"
    
    #Methods
    def __str__(self):
        """
        Return a readable representation of the hotel.
        """
        return self.name

    def get_available_rooms(self):
        """
        Returns the number of available rooms.
        """
        return self.available_rooms

    def book_room(self):
        """
        Reduces the number of available rooms when a booking is made.
        """
        if self.available_rooms > 0:
            self.available_rooms -= 1
            self.save()
            return True
        return False

    def cancel_booking(self):
        """
        Increases the number of available rooms when a booking is canceled.
        """
        if self.available_rooms < self.total_rooms:
            self.available_rooms += 1
            self.save()

    def has_availability(self):
        """
        Returns True if there are available rooms in the hotel.
        """
        return self.available_rooms > 0

    def get_amenities_list(self):
        """
        Returns a list of amenities as an array instead of a comma-separated string.
        """
        return [amenity.strip() for amenity in self.amenities.split(",")] if self.amenities else []

    def update_price(self, new_price):
        """
        Updates the price per night for the hotel.
        """
        if new_price > 0:
            self.price_night = new_price
            self.save()