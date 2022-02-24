from telnetlib import STATUS
from types import CoroutineType
from unicodedata import name
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings

class Lab(models.Model):

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name + ' Lab'

class Material(models.Model):

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name

class Specie(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name

#class Address(models.Model):
#    name        = models.CharField(max_length=30)
#    street      = models.CharField(max_length=200)
#    postal_code = models.CharField(max_length=10)
#    city        = models.CharField(max_length=30)
#    def __str__(self):
#        return self.name

class Address(models.Model):
    name        = models.CharField(max_length=200)
    street      = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    city        = models.CharField(max_length=30)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    #address = models.ForeignKey(Address, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Disposal_type(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name

class Dataset(models.Model):
    material            = models.ForeignKey(Material, null=False, blank=False, on_delete=models.CASCADE)
    specie              = models.ForeignKey(Specie, null=False, blank=False, on_delete=models.CASCADE)
    category            = models.CharField(max_length=2, choices=(
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ),default='3')    
    amount              = models.PositiveIntegerField()
    unit                = models.ForeignKey(Unit, null=False, blank=False, on_delete=models.CASCADE)
    point_of_origin     = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, related_name='origin_address')
    recipient           = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, related_name='recipient_address')
    date_of_disposal    = models.DateField(null=True, blank=True)
    disposal_type       = models.ForeignKey(Disposal_type, null=False, blank=False, on_delete=models.CASCADE)
    added_by            = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    creation_date       = models.DateTimeField(null=False, auto_now_add=True)
    lab                 = models.ForeignKey(Lab, null=False, blank=False, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab  = models.ForeignKey(Lab, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Book(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    co_authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='co_authored_by')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

