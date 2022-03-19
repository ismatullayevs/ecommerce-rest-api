from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	phone_number = PhoneNumberField(region="UZ", blank=True)

	def __str__(self):
		return self.user.username


class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	street_address = models.CharField(max_length=128)
	apartment_address = models.CharField(max_length=10)
	floor_number = models.PositiveIntegerField(blank=True, null=True)

	def __str__(self):
		return self.street
	


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile(user=instance)
		profile.save()