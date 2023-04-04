import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_pandas.models import Employee

class EmployeeViewSetTestCase(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            unique_id="A001",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            industry="Software",
            annual_income=50000,
            other_fields={"title": "Software Engineer"},
        )

        self.valid_payload = {
            "unique_id": "A002",
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1992-01-01",
            "industry": "Software",
            "annual_income": 60000,
            "other_fields": {"title": "Product Manager"},
        }

        self.invalid_payload = {
            "unique_id": "",
            "first_name": "",
            "last_name": "",
            "date_of_birth": "",
            "industry": "",
            "annual_income": "",
            "other_fields": {"title": ""},
        }

    def test_employee_list_view(self):
        response = self.client.get(reverse('employee-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_create_view(self):
        response = self.client.post(
            reverse('employee-list-create'),
            data=self.valid_payload,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_create_view_invalid_data(self):
        response = self.client.post(
            reverse('employee-list-create'),
            data=self.invalid_payload,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_retrieve_view(self):
        response = self.client.get(reverse('employee-retrieve-update-destroy', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_update_view(self):
        response = self.client.put(
            reverse('employee-retrieve-update-destroy', kwargs={'pk': self.employee.pk}),
            data=self.valid_payload,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_update_view_invalid_data(self):
        response = self.client.put(
            reverse('employee-retrieve-update-destroy',
                    kwargs={'pk': self.employee.pk}),data=self.invalid_payload,
                    format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_delete_view(self):
        response = self.client.delete(reverse('employee-retrieve-update-destroy', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_employee_create_view_negative_annual_income(self):
        negative_annual_income_payload = {
            'unique_id': '0123',
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1995-01-01',
            'industry': 'IT',
            'annual_income': -10000,
            'other_fields': {}
        }
        response = self.client.post(reverse('employee-list-create'), data=negative_annual_income_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('annual_income', response.data)
