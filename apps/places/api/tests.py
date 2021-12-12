from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.places.models import City, Workstation


class PlacesAPITestCase(APITestCase):
    CITY_LIST_URL = "/api/places/cities/"
    CITY_LIST_REVERSE = "city-list"
    CITY_UPDATE_URL = "/api/places/cities/{id}/"
    CITY_UPDATE_REVERSE = "city-detail"

    def setUp(self):
        City.objects.create(city="Wrocław")

    def test_urls_cities(self):
        self.assertEqual(self.CITY_LIST_URL, reverse(self.CITY_LIST_REVERSE))
        self.assertEqual(
            self.CITY_UPDATE_URL.format(id=1),
            reverse(self.CITY_UPDATE_REVERSE, kwargs={"pk": 1}),
        )

    def test_create_city(self):
        data = {"city": "Daleko"}
        response = self.client.post(reverse(self.CITY_LIST_REVERSE), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"city": "Inne"}
        previous = City.objects.count()
        response = self.client.post(
            reverse(self.CITY_LIST_REVERSE), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(City.objects.count(), previous + 1)

    def test_update_city(self):
        city = City.objects.create(city="Inne")
        response = self.client.patch(
            reverse(self.CITY_UPDATE_REVERSE, kwargs={"pk": city.id}),
            {"city": "Daleko"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(
            reverse(self.CITY_UPDATE_REVERSE, kwargs={"pk": city.id}),
            {"city": "Rzeszów"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(City.objects.get(pk=city.pk).city, City.CityName.RZESZOW)

    def test_retrieve_city(self):
        city = City.objects.create(city="Inne")
        response = self.client.get(
            reverse(self.CITY_UPDATE_REVERSE, kwargs={"pk": city.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], City.CityName.INNE)

    def test_delete_city(self):
        city = City.objects.first()
        previous = City.objects.count()
        response = self.client.delete(
            reverse(self.CITY_UPDATE_REVERSE, kwargs={"pk": city.id})
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(City.objects.count(), previous)

    def test_list_city(self):

        keys = ["id", "city", "is_active"]
        response = self.client.get(reverse(self.CITY_LIST_REVERSE))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
        for key in keys:
            self.assertTrue(key in response.data[0])


class WorkstationAPITestCase(APITestCase):
    WORKSTATION_LIST_URL = "/api/places/workstations/"
    WORKSTATION_LIST_REVERSE = "workstation-list"
    WORKSTATION_UPDATE_URL = "/api/places/workstations/{id}/"
    WORKSTATION_UPDATE_REVERSE = "workstation-detail"

    def setUp(self):
        Workstation.objects.create(workstation="UX Designer")
        Workstation.objects.create(workstation="UI Designer")

    def test_urls_workstation(self):
        self.assertEqual(
            self.WORKSTATION_LIST_URL, reverse(self.WORKSTATION_LIST_REVERSE)
        )
        self.assertEqual(
            self.WORKSTATION_UPDATE_URL.format(id=1),
            reverse(self.WORKSTATION_UPDATE_REVERSE, kwargs={"pk": 1}),
        )

    def test_create_workstation(self):
        data = {"workstation": "C#"}
        response = self.client.post(reverse(self.WORKSTATION_LIST_REVERSE), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        previous = Workstation.objects.count()
        data = {"workstation": "Python"}
        response = self.client.post(
            reverse(self.WORKSTATION_LIST_REVERSE), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workstation.objects.count(), previous + 1)

    def test_update_workstation(self):
        workstation = Workstation.objects.create(workstation="PHP")
        response = self.client.patch(
            reverse(self.WORKSTATION_UPDATE_REVERSE, kwargs={"pk": workstation.id}),
            {"workstation": "C#"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(
            reverse(self.WORKSTATION_UPDATE_REVERSE, kwargs={"pk": workstation.id}),
            {"workstation": "Python"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Workstation.objects.get(pk=workstation.pk).workstation,
            Workstation.WorkstationName.PYTHON,
        )

    def test_retrieve_workstation(self):
        workstation = Workstation.objects.create(workstation="PHP")
        response = self.client.get(
            reverse(self.WORKSTATION_UPDATE_REVERSE, kwargs={"pk": workstation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["workstation"], workstation.workstation)

    def test_delete_workstation(self):
        workstation = Workstation.objects.first()
        previous = Workstation.objects.count()
        response = self.client.delete(
            reverse(self.WORKSTATION_UPDATE_REVERSE, kwargs={"pk": workstation.id})
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Workstation.objects.count(), previous)

    def test_list_workstation(self):

        keys = ["id", "workstation", "is_active"]
        response = self.client.get(reverse(self.WORKSTATION_LIST_REVERSE))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
        for key in keys:
            self.assertTrue(key in response.data[0])
