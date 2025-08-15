from django.conf import settings
from django.db import models


class Play(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Title:{self.title}, Description:{self.description}"


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return f"Name:{self.name}, Rows:{self.rows}, Seats:{self.seats_in_row}"


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"Play:{self.play}, TheatreHall:{self.theatre_hall}, Show Time:{self.show_time}"


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    play = models.ManyToManyField(Play)

    def __str__(self):
        return f"First Name:{self.first_name}, Last Name:{self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=100)
    play = models.ManyToManyField(Play)

    def __str__(self):
        return f"Name:{self.name}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"User:{self.user}, Reservation:{self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance =models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    def __str__(self):
        return f"Row: {self.row}, Seat: {self.seat}, Performance: {self.performance}, Reservation: {self.reservation} "