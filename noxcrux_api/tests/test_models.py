from rest_framework.test import APITestCase
from noxcrux_api.models.Horcrux import Horcrux
from noxcrux_api.models.Generator import Generator
from noxcrux_api.models.Friend import Friend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TestModels(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='test', password='test')
        cls.friend = User.objects.create_user(username='test_friend', password='test_friend')
        cls.horcrux_data = {'name': 'Google', 'horcrux': 'a5v8t4d', 'site': 'https://google.com', 'owner': cls.test_user}

    def test_horcrux_str(self):
        horcrux = Horcrux.objects.create(**self.horcrux_data)
        self.assertEqual('Google', str(horcrux))

    def test_generator_str(self):
        self.assertEqual('test', str(Generator.objects.get(owner=self.test_user)))

    def test_validated_friend_str(self):
        friendship = Friend.objects.create(user=self.test_user, friend=self.friend, validated=True)
        self.assertEqual(f"User {self.test_user} is friend with {self.friend}", str(friendship))

    def test_non_validated_friend_str(self):
        friendship = Friend.objects.create(user=self.test_user, friend=self.friend, validated=False)
        self.assertEqual(f"User {self.test_user} is waiting to be friend with {self.friend}", str(friendship))

    def test_self_friend_exception(self):
        with self.assertRaises(ValidationError):
            Friend.objects.create(user=self.test_user, friend=self.test_user, validated=False)
