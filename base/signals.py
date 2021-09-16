from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from .models import UserProfile, OnlineClass


def create_profile(sender, instance, created, **kwargs):
	c = OnlineClass.objects.get(name="بدون کلاس")
	if created:
		user=UserProfile.objects.create(
			user=instance,
			)	
		print('Profile Created!')

post_save.connect(create_profile, sender=User)
