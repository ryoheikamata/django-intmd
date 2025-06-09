from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from matching_app.models import User, UserVerification


class SignupViewTests(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username="existing_user",
            email="existing@example.com",
            password="ExistingPass123",
            date_of_birth="2000-01-01",
        )

        self.signup_url = reverse("signup")

    def test_signup_success(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "new_user",
                "email": "new@example.com",
                "password": "NewPass123",
                "date_of_birth": "2000-01-01",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

        new_user = User.objects.get(email="new@example.com")

        self.assertRedirects(response, reverse("verify_email", args=[new_user.id]))
        self.assertFalse(new_user.is_active)

    def test_signup_failure_with_existing_user(self):
        response = self.client.post(
            self.signup_url,
            {
                "username": "existing_user",
                "email": "existing@example.com",
                "password": "ExistingPass123",
                "date_of_birth": "2000-01-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup_error.html")


class VerifyViewTests(TestCase):
    def setUp(self):
        self.verify_user = get_user_model().objects.create_user(
            username="verify_user",
            email="verify@example.com",
            password="VerifyPass123",
            date_of_birth="2000-01-01",
            is_active=False,
        )
        self.user_verification = self.verify_user.userverification
        self.user_verification.verification_code = "123456"
        self.user_verification.save()

        self.verify_url = reverse("verify_email", args=[self.verify_user.id])
        self.send_verification_url = reverse("send_new_verification_code", args=[self.verify_user.id])
        self.user_home_url = reverse("user_home")

    def test_verify_email_success(self):
        response = self.client.post(
            self.verify_url,
            {
                "verification_code": "123456",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.user_home_url)
        self.assertFalse(UserVerification.objects.filter(user=self.verify_user).exists())

    def test_verify_email_failure_with_invalid_code(self):
        response = self.client.post(
            self.verify_url,
            {
                "verification_code": "000000",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "verify_email.html")
        self.assertNotEqual(self.user_verification.verification_code, "000000")

        got_verify_user = User.objects.get(id=self.verify_user.id)
        self.assertFalse(got_verify_user.is_active)


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="login_user",
            email="login@example.com",
            password="LoginPass123",
            date_of_birth="2000-01-01",
        )
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.user_home_url = reverse("user_home")
        self.index_url = reverse("index")

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "login@example.com",
                "password": "LoginPass123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.user_home_url)
        self.assertTrue(User.objects.filter(username="login_user").exists())

    def test_login_failure_with_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "login@example.com",
                "password": "InvalidPass123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login_error.html")

    def test_logout_success(self):
        self.client.post(
            self.login_url,
            {
                "email": "login@example.com",
                "password": "LoginPass123",
            },
        )

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
