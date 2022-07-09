from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures") 
    #the above (on_delete = models.cascade) tells django what should happen
    #to the flight if the thing it is referencing is deleted
    #the related name allows for searches in reverse order eg from origin
    #which other flights are leaving too.
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.id}: {self.origin} to {self.destination}"

class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")
    #blank=True means its possible for a passenger to have no flights at all

    def __str__(self) -> str:
        return  f'{self.first} {self.last}'