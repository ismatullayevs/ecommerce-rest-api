from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User


class UserTestCase(TestCase):
	def setUp(self):
		User.objects.create_user(username="djangostars", password="my_pass", email="example@gmail.com")
		User.objects.create_superuser(username="adminn")

	def test_user(self):
		user = User.objects.get(username="djangostars")
		self.assertEqual(user.username, "djangostars")
		self.assertEqual(user.email, "example@gmail.com")
		self.assertEqual(user.is_staff, False)

	def test_admin_user(self):
		admin = User.objects.get(username="adminn")
		self.assertEqual(admin.is_staff, True)



class ProfileTestCase(TestCase):
	def setUp(self):
		User.objects.create_user(username="djangostars", password="my_pass", email="example@gmail.com")

	def test_profile_creation(self):
		user = User.objects.get(username="djangostars")
		self.assertEqual(user.username, user.profile.user.username)

	def test_phone_number(self):
		profile = Profile.objects.get(user__username="djangostars")
		profile.phone_number = "+998936511499"
		self.assertEqual(profile.phone_number, "+998936511499")