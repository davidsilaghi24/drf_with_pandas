from django.test import TestCase
from api_pandas.models import Employee
from datetime import date

class EmployeeModelTestCase(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            unique_id="EMP001",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            industry="Technology",
            annual_income=50000.00,
            other_fields={"title": "Software Developer"},
        )

    def test_employee_created_successfully(self):
        self.assertEqual(self.employee.unique_id, "EMP001")
        self.assertEqual(self.employee.first_name, "John")
        self.assertEqual(self.employee.last_name, "Doe")
        self.assertEqual(self.employee.date_of_birth, date(1990, 1, 1))
        self.assertEqual(self.employee.industry, "Technology")
        self.assertEqual(self.employee.annual_income, 50000.00)
        self.assertEqual(self.employee.other_fields, {"title": "Software Developer"})

    def test_employee_years_of_experience(self):
        today = date.today()
        age = today.year - self.employee.date_of_birth.year - (
            (today.month, today.day) < (self.employee.date_of_birth.month, self.employee.date_of_birth.day)
        )
        self.assertEqual(self.employee.years_of_experience, age)

    def test_employee_string_representation(self):
        self.assertEqual(str(self.employee), "John Doe - EMP001")
