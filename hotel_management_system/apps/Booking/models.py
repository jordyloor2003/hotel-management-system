from django.db import models
from ..User.models import User
from ..Hotel.models import Hotel
from django.utils.timezone import now

class Booking(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELED, 'Canceled'),
    )

    #Fields
    customer = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bookings")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank= True, null= True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    

    #Metadata
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    #Methods
    def __str__(self):
        """
        Returns a readable representation of the booking.
        """
        return f"{self.customer.username} - {self.hotel.name} ({self.check_in} to {self.check_out})"

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError("Check-in date must be before check-out date.")

    def get_total_price(self):
        """
        Calculate the total price of the reservation based on the number of nights.
        """
        nights = (self.check_out - self.check_in).days
        return self.hotel.price_night * nights if nights > 0 else 0
    
    def get_duration(self):
        """
        Returns the number of nights booked.
        """
        duration = (self.check_out - self.check_in).days
        return duration if self.check_out and self.check_in else 0
    
    def is_active(self):
        """
        Returns True if the reservation is confirmed and the departure date has not passed.
        """
        return self.status == self.CONFIRMED and self.check_out >= now().date()
    
    def cancel_booking(self):
        """
        Change the reservation status to 'canceled'.
        """
        if self.status != self.CANCELED:
            self.status = self.CANCELED
            self.save()

    def confirm_booking(self):
        """
        Change the reservation status to 'confirmed'.
        """
        if self.status == self.PENDING:
            self.status = self.CONFIRMED
            self.save()

    def has_checked_in(self):
        """
        Return True if today is check-in day or has already passed.
        """
        return now().date() >= self.check_in

    def has_checked_out(self):
        """
        Return True if the release date has passed.
        """
        return now().date() > self.check_out