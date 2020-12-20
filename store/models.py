from django.db import models

# Create your models here.

class Contact(models.Model):
  phone_number = models.CharField(max_length=100)
  mail = models.EmailField(max_length=100)
  name = models.CharField(max_length=200)

  class Meta:
    verbose_name = "prospect"

  def __str__(self):
    return self.name

ListeType = (
    ('diesel', 'Diesel'),
    ('essance', 'Essence '),
)

class Car(models.Model):
  reference = models.IntegerField(blank=False, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  available = models.BooleanField(default=True)
  title = models.CharField(max_length=200)
  petrol = models.CharField(max_length=10, choices=ListeType, default='diesel')
  KM = models.IntegerField(blank=False, null=True)
  picture = models.ImageField(upload_to='upload')

  class Meta:
    verbose_name = "voiture"

  def __str__(self):
    return self.title


class Rental(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  contacted = models.BooleanField(default=False)
  car = models.OneToOneField(Car, on_delete=models.CASCADE)
  contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

  class Meta:
    verbose_name = "réservation"

  def __str__(self):
    return self.contact.name