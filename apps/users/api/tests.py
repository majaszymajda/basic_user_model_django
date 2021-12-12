from django.urls import reverse

from knox.models import AuthToken
from rest_framework.test import APITestCase

from apps.places.models import City, Workstation
from apps.users.models import Profile, User


class TestUserAPI(APITestCase):
    USER_LIST_URL = "/api/users/users/"  # IS_AUTHENTICATED
    USER_RETRIEVE_URL = "/api/users/users/{id}/"  # IS_AUTHENTICATED
    USER_FORGOT_PASSWORD_URL = "/api/users/users/forgot-password/"  # CURRENT_USER
    USER_UPDATE_CREDENTIALS_URL = "/api/users/users/{id}/credentials/"  # ADMIN -> first_name, last_name, is_active, is_removed
    USER_UPDATE_PASSWORD_URL = "/api/users/users/{id}/password/"  # CURRENT_USER -> old_password <=> new_password == confirm_new_password

    USER_REGISTER_URL = "/api/auth/register/"  # ALL
    USER_LOGIN_URL = "/api/auth/login/"  # ALL
    USER_LOGOUT_URL = "/api/auth/logout/"  # CURRENT_USER

    PROFILE_LIST_URL = "/api/users/profiles/"  # IS_AUTHENTICATED
    PROFILE_RETRIEVE_URL = "/api/users/profiles/{id}/"  # IS_AUTHENTICATED
    PROFILE_UPDATE_URL = "/api​/users​/profiles​/{id}​/update​/"  # CURRENT_USER -> workstations, workcity

    USER_USERNAME = "test"
    USER_PASSWORD = "password"
    USER_EMAIL = "user@test.com"

    USER_2_USERNAME = "second"
    USER_2_PASSWORD = "second"
    USER_2_EMAIL = "second@test.com"

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "password"
    ADMIN_EMAIL = "admin@test.com"

    @classmethod
    def setUpTestData(self):
        self.workcity = City.objects.create(city=City.CityName.WROCLAW, is_active=True)
        self.workcity2 = City.objects.create(
            city=City.CityName.RZESZOW, is_active=False
        )
        self.workstation1 = Workstation.objects.create(
            workstation=Workstation.WorkstationName.UX, is_active=False
        )
        self.workstation2 = Workstation.objects.create(
            workstation=Workstation.WorkstationName.UI, is_active=False
        )
        self.workstation3 = Workstation.objects.create(
            workstation=Workstation.WorkstationName.PHP, is_active=True
        )
        self.workstation4 = Workstation.objects.create(
            workstation=Workstation.WorkstationName.PYTHON, is_active=True
        )

        admin_username = self.ADMIN_USERNAME
        admin_password = self.ADMIN_PASSWORD
        admin_email = self.ADMIN_EMAIL

        admin = User.objects.create_superuser(
            username=admin_username, email=admin_email, password=admin_password
        )
        self.admin = admin
        user_username = self.USER_USERNAME
        user_password = self.USER_PASSWORD
        user_email = self.USER_EMAIL
        user_first_name = "test"
        user_last_name = "test"

        user = User.objects.create(
            username=user_username,
            password=user_password,
            first_name=user_first_name,
            last_name=user_last_name,
            email=user_email,
        )
        user.set_password(self.USER_PASSWORD)
        user.save()
        profile = user.profile
        profile.workstations.add(self.workstation1)
        profile.workstations.add(self.workstation2)
        self.user = user

        user_2_username = self.USER_2_USERNAME
        user_2_password = self.USER_2_PASSWORD
        user_2_email = self.USER_2_EMAIL
        user_2_first_name = "second"
        user_2_last_name = "second"

        user2 = User.objects.create(
            username=user_2_username,
            password=user_2_password,
            first_name=user_2_first_name,
            last_name=user_2_last_name,
            email=user_2_email,
        )
        user2.set_password(self.USER_2_PASSWORD)
        user2.save()
        self.user2 = user2

    def login_admin(self):
        self.client.login(email=self.ADMIN_EMAIL, password=self.ADMIN_PASSWORD)
        self.token = AuthToken.objects.create(user=self.admin)[1]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def login_user(self):
        self.client.login(email=self.USER_2_EMAIL, password=self.USER_PASSWORD)
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_create_account_and_duplicate_data(self):
        url = reverse("knox_register")
        previous_users_count = User.objects.count()
        previous_profiles_count = Profile.objects.count()
        username = "test2"
        first_name = "test2"
        last_name = "test2"
        valid_email = "valid@valid.com"
        valid_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": valid_email,
        }
        duplicate_account_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": valid_email,
        }
        response = self.client.post(url, valid_data, format="json")
        self.assertEqual(
            response.status_code, 201
        )  # poprawne dane rejestracji !!!! TRZEBA ZMIENIC RESPONSE NA 201 W WIDOKU !!!!
        self.assertEqual(User.objects.count(), previous_users_count + 1)
        self.assertEqual(Profile.objects.count(), previous_profiles_count + 1)
        self.assertEqual(User.objects.last().username, username)
        response = self.client.post(url, duplicate_account_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # próba rejestracji z istniejącym username

    def test_create_account_bad_data(self):
        url = reverse("knox_register")
        invalid_data = {
            "username": "test2",
            "first_name": "test2",
            "last_name": "test2",
            "email": "email",
        }
        response = self.client.post(url, invalid_data, format="json")
        self.assertEqual(response.status_code, 400)  # zły email

    def test_login_account(self):
        url = reverse("knox_login")
        previous_tokens_count = AuthToken.objects.count()
        valid_data = {"email": self.USER_EMAIL, "password": self.USER_PASSWORD}
        response = self.client.post(url, valid_data, format="json")
        self.assertEqual(response.status_code, 200)  # poprawne dane logowania
        self.assertEqual("token" in response.data.keys(), True)
        self.assertEqual(AuthToken.objects.count(), previous_tokens_count + 1)

    def test_login_bad_password(self):
        url = reverse("knox_login")
        invalid_password_data = {
            "email": self.USER_EMAIL,
            "password": "wrong_test",
        }
        response = self.client.post(url, invalid_password_data, format="json")
        self.assertEqual(response.status_code, 400)  # złe hasło

    def test_login_bad_email(self):
        url = reverse("knox_login")
        invalid_email_data = {
            "email": "wrong_test",
            "password": self.USER_PASSWORD,
        }
        response = self.client.post(url, invalid_email_data, format="json")
        self.assertEqual(response.status_code, 400)  # zły username

    def test_logout_account(self):
        url = reverse("knox_logout")
        self.login_user()
        previous_tokens_count = AuthToken.objects.count()
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(AuthToken.objects.count(), previous_tokens_count - 1)

    def test_retrieve_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 401)  # before log in
        self.login_user()
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)  # after log in, for current user

    def test_retrieve_user_not_exists(self):
        url = reverse("user-detail", kwargs={"pk": 10})
        self.login_user()
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.status_code, 404
        )  # trying to retrieve user that doesnt exist

    def test_list_user(self):
        url = reverse("user-list")
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.status_code, 401
        )  # Trying to get list of users before log in

        self.login_user()
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.status_code, 200
        )  # Trying to get list of users after log in
        self.assertEqual(response.data["count"], 3)

    def test_update_password_old_bad(self):
        old_bad_data = {
            "old_password": "bad_password",
            "new_password": "new_password",
            "confirm_password": "new_password",
        }
        url = reverse("user-update-password", kwargs={"pk": self.user.pk})
        self.login_user()
        response = self.client.put(url, old_bad_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update password with wrong old password

    def test_update_password_new_bad(self):
        new_bad_data = {
            "old_password": self.USER_PASSWORD,
            "new_password": self.USER_PASSWORD,
            "confirm_password": "new_password",
        }
        url = reverse("user-update-password", kwargs={"pk": self.user.pk})
        self.login_user()
        response = self.client.put(url, new_bad_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update password with new password set to old password

    def test_update_password_new_short_bad(self):
        short_bad_data = {
            "old_password": self.USER_PASSWORD,
            "new_password": "t",
            "confirm_password": "t",
        }
        url = reverse("user-update-password", kwargs={"pk": self.user.pk})
        self.login_user()
        response = self.client.put(url, short_bad_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update password with to short password

    def test_update_password_confirmed_bad(self):
        confirmed_bad_data = {
            "old_password": self.USER_PASSWORD,
            "new_password": "new_password",
            "confirm_password": "new_bad_password",
        }
        url = reverse("user-update-password", kwargs={"pk": self.user.pk})
        self.login_user()
        response = self.client.put(url, confirmed_bad_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update password with badly confirmed password

    def test_update_password_incomplete_bad(self):
        incomplete_bad_data = {
            "old_password": self.USER_PASSWORD,
            "new_password": "new_password",
        }
        url = reverse("user-update-password", kwargs={"pk": self.user.pk})
        self.login_user()
        response = self.client.put(url, incomplete_bad_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update password with incomplete data

    def test_update_password_another_user(self):
        user2_data = {
            "old_password": self.USER_2_PASSWORD,
            "new_password": "new_second",
            "confirm_password": "new_second",
        }
        url = reverse("user-update-password", kwargs={"pk": self.user2.pk})
        self.login_user()
        response = self.client.put(url, user2_data, format="json")
        self.assertEqual(
            response.status_code, 403
        )  # Trying to update password of another user !!!

    def test_update_password_user_not_exist(self):
        correct_data = {
            "old_password": self.USER_PASSWORD,
            "new_password": "new_password",
            "confirm_password": "new_password",
        }
        url = reverse("user-update-password", kwargs={"pk": 5})
        self.login_user()
        response = self.client.put(url, correct_data, format="json")
        self.assertEqual(
            response.status_code, 404
        )  # Trying to update password of a user that doesnt exist

    def test_update_password_user(self):
        url = reverse("user-update-password", kwargs={"pk": self.user.pk})

        correct_data = {
            "old_password": self.USER_PASSWORD,
            "new_password": "new_password",
            "confirm_password": "new_password",
        }

        response = self.client.put(
            url.format(id=self.user.id), correct_data, format="json"
        )
        self.assertEqual(
            response.status_code, 401
        )  # Trying to update password without being logged in
        self.login_user()
        response = self.client.put(
            url.format(id=self.user.id), correct_data, format="json"
        )
        self.assertEqual(
            response.status_code, 200
        )  # Trying to update password with correct data

    def test_update_credentials_user_not_authorized(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        correct_data = {
            "is_active": True,
            "first_name": "new_first_name",
            "last_name": "new_last_name",
        }

        response = self.client.put(
            url.format(id=self.user.id), correct_data, format="json"
        )
        self.assertEqual(
            response.status_code, 401
        )  # Trying to update user credentials without being logged in

        self.login_user()
        response = self.client.put(
            url.format(id=self.user.id), correct_data, format="json"
        )
        self.assertEqual(
            response.status_code, 403
        )  # Trying to update user credentials without being logged in as admin (logged in as user)

    def test_update_credentials_user_not_exists(self):
        url = reverse("user-detail", kwargs={"pk": 5})
        correct_data = {
            "is_active": True,
            "first_name": "new_first_name",
            "last_name": "new_last_name",
        }
        self.login_admin()
        response = self.client.put(url, correct_data, format="json")
        self.assertEqual(
            response.status_code, 404
        )  # Trying to update credentials of a user that doesnt exist

    def test_update_credentials_good(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        correct_data = {
            "is_active": True,
            "first_name": "new_first_name",
            "last_name": "new_last_name",
        }
        self.login_admin()
        response = self.client.put(
            url.format(id=self.user.id), correct_data, format="json"
        )
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(
            response.status_code, 200
        )  # Trying to update password with correct data
        self.assertEqual(user.is_active, correct_data["is_active"])
        self.assertEqual(user.first_name, correct_data["first_name"])
        self.assertEqual(user.last_name, correct_data["last_name"])

    def test_update_credentials_bad_is_active(self):
        url = reverse("user-detail", kwargs={"pk": self.user.pk})
        self.login_admin()
        is_active_bad_data = {
            "is_active": "bad_is_active",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
        }
        response = self.client.put(
            url.format(id=self.user.id), is_active_bad_data, format="json"
        )
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update credentials with not valid is_active field
        self.assertTrue("is_active" in response.data)

    def test_retrieve_profile(self):
        self.login_user()
        profile = Profile.objects.get(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": profile.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.status_code, 200
        )  # trying to retrieve profile that exists
        self.assertEqual(
            response.data["id"], profile.id
        )  # checking if returned profile is the one that we asked for

    def test_retrieve_profile_not_exists(self):
        self.login_user()
        url = reverse("profile-detail", kwargs={"pk": 10})
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.status_code, 404
        )  # trying to retrieve profile that doesnt exist

    def test_list_profile(self):
        self.login_user()
        url = reverse("profile-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

    def test_update_profile_not_logged(self):
        profile = Profile.objects.get(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": profile.pk})
        correct_data = {
            "work_city": self.workcity2.id,
            "workstations": [self.workstation3.id, self.workstation4.id],
        }
        response = self.client.put(url, correct_data, format="json")
        self.assertEqual(
            response.status_code, 401
        )  # Trying to update profile without being logged in

    def test_update_profile_not_exist(self):
        url = reverse("profile-detail", kwargs={"pk": 10})
        correct_data = {
            "work_city": self.workcity2.id,
            "workstations": [self.workstation3.id, self.workstation4.id],
        }
        self.login_user()
        response = self.client.put(url, correct_data, format="json")
        self.assertEqual(
            response.status_code, 404
        )  # Trying to update profile that doesnt exist

    def test_update_profile_bad_workcity(self):
        profile = Profile.objects.get(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": profile.pk})
        workcity_bad_data = {
            "work_city": "bad_workcity",
            "workstations": [self.workstation3.id, self.workstation4.id],
        }
        workcity_bad_indexes_data = {
            "work_city": City.objects.last().id + 1,
            "workstations": [self.workstation3.id, self.workstation4.id],
        }
        self.login_user()
        response = self.client.put(url, workcity_bad_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update profile with wrong workcity data
        response = self.client.put(url, workcity_bad_indexes_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update profile with workcity that doesnt exist

    def test_update_profile_bad_workstations(self):
        profile = Profile.objects.get(user=self.user)
        url = reverse("profile-detail", kwargs={"pk": profile.pk})
        workstations_bad_data = {
            "work_city": self.workcity2.id,
            "workstations": "bad_workstations",
        }
        workstations_bad_indexes_data = {
            "work_city": self.workcity2.id,
            "workstations": [Workstation.objects.last().id + 1],
        }
        self.login_user()
        response = self.client.put(url, workstations_bad_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update profile with wrong workstations data
        response = self.client.put(url, workstations_bad_indexes_data, format="json")
        self.assertEqual(
            response.status_code, 400
        )  # Trying to update profile with workstations that doesnt exist

    def test_update_profile(self):
        profile = Profile.objects.get(user=self.user)
        profile2 = Profile.objects.get(user=self.user2)
        url = reverse("profile-detail", kwargs={"pk": profile2.pk})
        correct_data = {
            "work_city": self.workcity2.id,
            "workstations": [self.workstation3.id, self.workstation4.id],
        }
        self.login_user()
        response = self.client.put(url, correct_data, format="json")
        self.assertEqual(
            response.status_code, 403
        )  # Trying to update profile of another user !!!
        url = reverse("profile-detail", kwargs={"pk": profile.pk})
        response = self.client.put(url, correct_data, format="json")
        self.assertEqual(
            response.status_code, 200
        )  # Trying to update profile with correct data
