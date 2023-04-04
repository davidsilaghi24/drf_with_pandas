import os, json, datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_pandas.models import Employee

class EmployeeViewSetTestCase(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime.date(1990, 1, 1),
            industry="Software",
            salary=50000,
            years_of_experience=10,
            other_fields={"title": "Software Engineer"},
        )

        # Create 9 more employees
        for i in range(2, 11):
            Employee.objects.create(
                first_name=f"Employee{i}",
                last_name="Doe",
                date_of_birth=datetime.date(1990, 1, 1),
                industry="Software",
                salary=50000,
                years_of_experience=10,
                other_fields={"title": "Software Engineer"},
            )

        self.valid_payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1992-01-01",
            "industry": "Software",
            "salary": 60000,
            "years_of_experience": 10,
            "other_fields": {"title": "Product Manager"},
        }

        self.invalid_payload = {
            "first_name": "",
            "last_name": "",
            "date_of_birth": "",
            "industry": "",
            "salary": "",
            "years_of_experience": "",
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
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1995-01-01',
            'industry': 'IT',
            'salary': -10000,
            'other_fields': {}
        }
        response = self.client.post(reverse('employee-list-create'), data=negative_annual_income_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('salary', response.data)

    def test_employee_list_pagination(self):
        response = self.client.get(reverse('employee-list-create'), {'page': 2, 'page_size': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_search(self):
        response = self.client.get(reverse('employee-list-create'), {'search': 'Doe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_ordering(self):
        response = self.client.get(reverse('employee-list-create'), {'ordering': 'first_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_filtering(self):
        response = self.client.get(reverse('employee-list-create'), {'industry': 'IT'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MockedDataCRUDTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Load the mocked_data.json file
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        mocked_data_file_path = os.path.join(current_file_path, 'MOCK_DATA.json')

        with open(mocked_data_file_path, 'r') as file:
            cls.mocked_data = json.load(file)[:500]

    def test_crud_employees_from_mocked_data(self):
        # test_create_employees_from_mocked_data
        for employee_data in self.mocked_data:
            response = self.client.post(
                reverse('employee-list-create'),
                data=employee_data,
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test_retrieve_employees_from_mocked_data
        for employee_data in self.mocked_data:
            response = self.client.get(reverse('employee-retrieve-update-destroy', kwargs={'pk': employee_data['id']}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test_update_employees_from_mocked_data
        for employee_data in self.mocked_data:
            # Update salary
            updated_employee_data = employee_data.copy()
            updated_employee_data['salary'] = (float(employee_data['salary']) if employee_data['salary'] is not None else 0) + 1000

            response = self.client.put(
                reverse('employee-retrieve-update-destroy', kwargs={'pk': employee_data['id']}),
                data=updated_employee_data,
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test_delete_employees_from_mocked_data
        for employee_data in self.mocked_data:
            response = self.client.delete(reverse('employee-retrieve-update-destroy', kwargs={'pk': employee_data['id']}))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
