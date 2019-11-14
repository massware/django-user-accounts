from django.contrib.auth.models import User
from django.test import TestCase

from account.forms import LoginEmailForm

from ..forms import SignupEmailForm, SignupForm


class SignupFormTestCase(TestCase):
    def test_is_valid(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
        }
        form = SignupForm(data=data)

        self.assertEqual(form.is_valid(), True)

    def test_not_valid(self):
        data = {
            "username": "foo",
            "password_confirm": "bar",
            "email": "foobar@example.com",
        }
        form = SignupForm(data=data)

        self.assertEqual(form.is_valid(), False)

    def test_username_exists_error(self):
        User.objects.create_user("foo", password="bar")
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
        }
        form = SignupForm(data=data)

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors, {"username": ["This username is already taken. Please choose another."]})

    def test_username_alnum_error(self):
        data = {
            "username": "foo@!",
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
        }
        form = SignupForm(data=data)

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors, {"username": ["Usernames can only contain letters, numbers and underscores."]})


class SignupEmailFormTestCase(TestCase):
    def test_is_valid(self):
        data = {
            "password": "bar",
            "password_confirm": "bar",
            "email": "foobar@example.com",
        }
        form = SignupEmailForm(data=data)

        self.assertEqual(form.is_valid(), True)

    def test_not_valid(self):
        data = {
            "username": "foo",
            "password": "bar",
            "password_confirm": "bar",
        }
        form = SignupEmailForm(data=data)

        self.assertEqual(form.is_valid(), False)


class LoginEmailTestCase(TestCase):
    def test_is_valid(self):
        User.objects.create_user(username="foo@example.com", password="bar", email="foo@example.com")
        data = {
            "password": "bar",
            "email": "foo@example.com",
            "code": "abc123",
        }
        form = LoginEmailForm(data=data)

        self.assertEqual(form.is_valid(), True)
