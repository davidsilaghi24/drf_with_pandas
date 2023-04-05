from django.test import TestCase
from api_pandas.models import Employee
from datetime import date


class EmployeeModelTestCase(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            industry="Technology",
            salary=50000.00,
            other_fields={"title": "Software Developer"},
        )

    def test_employee_created_successfully(self):
        self.assertEqual(self.employee.first_name, "John")
        self.assertEqual(self.employee.last_name, "Doe")
        self.assertEqual(self.employee.date_of_birth, date(1990, 1, 1))
        self.assertEqual(self.employee.industry, "Technology")
        self.assertEqual(self.employee.salary, 50000.00)
        self.assertEqual(
            self.employee.other_fields,
            {"title": "Software Developer"}
            )
