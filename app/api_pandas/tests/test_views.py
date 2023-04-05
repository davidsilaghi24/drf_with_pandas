import os
import json
import datetime
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
        response = self.client.get(reverse("employee-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_create_view(self):
        response = self.client.post(
            reverse("employee-list-create"),
            data=self.valid_payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_create_view_invalid_data(self):
        response = self.client.post(
            reverse("employee-list-create"),
            data=self.invalid_payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_retrieve_view(self):
        response = self.client.get(
            reverse(
                "employee-retrieve-update-destroy",
                kwargs={"pk": self.employee.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_update_view(self):
        response = self.client.put(
            reverse(
                "employee-retrieve-update-destroy",
                kwargs={"pk": self.employee.pk}
            ),
            data=self.valid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_update_view_invalid_data(self):
        response = self.client.put(
            reverse(
                "employee-retrieve-update-destroy",
                kwargs={"pk": self.employee.pk}
            ),
            data=self.invalid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_delete_view(self):
        response = self.client.delete(
            reverse(
                "employee-retrieve-update-destroy",
                kwargs={"pk": self.employee.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_employee_create_view_negative_annual_income(self):
        negative_annual_income_payload = {
            "first_name": "Test",
            "last_name": "User",
            "date_of_birth": "1995-01-01",
            "industry": "IT",
            "salary": -10000,
            "other_fields": {},
        }
        response = self.client.post(
            reverse("employee-list-create"),
            data=negative_annual_income_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("salary", response.data)

    def test_employee_list_pagination(self):
        response = self.client.get(
            reverse("employee-list-create"),
            {"page": 2, "page_size": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_search(self):
        response = self.client.get(
            reverse("employee-list-create"),
            {"search": "Doe"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_ordering(self):
        response = self.client.get(
            reverse("employee-list-create"),
            {"ordering": "first_name"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_list_filtering(self):
        response = self.client.get(
            reverse("employee-list-create"),
            {"industry": "IT"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MockedDataCRUDTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Load the mocked_data.json file
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        mocked_data_file_path = os.path.join(
            current_file_path, "MOCK_DATA.json"
            )

        with open(mocked_data_file_path, "r") as file:
            cls.mocked_data = json.load(file)[:500]

    def test_crud_employees_from_mocked_data(self):
        # test_create_employees_from_mocked_data
        for employee_data in self.mocked_data:
            response = self.client.post(
                reverse("employee-list-create"),
                data=employee_data,
                format="json"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test_retrieve_employees_from_mocked_data
        for employee_data in self.mocked_data:
            response = self.client.get(
                reverse(
                    "employee-retrieve-update-destroy",
                    kwargs={"pk": employee_data["id"]},
                )
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test_update_employees_from_mocked_data
        for employee_data in self.mocked_data:
            # Update salary
            updated_employee_data = employee_data.copy()
            updated_employee_data["salary"] = (
                float(employee_data["salary"])
                if employee_data["salary"] is not None
                else 0
            ) + 1000

            response = self.client.put(
                reverse(
                    "employee-retrieve-update-destroy",
                    kwargs={"pk": employee_data["id"]},
                ),
                data=updated_employee_data,
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test_average_age_per_industry
        response = self.client.get(reverse("average-age-per-industry"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assertions to check response data for average_age_per_industry
        data = response.json()

        advertising = next(
            item
            for item in data
            if item["industry"]
            == "Advertising"
            )
        self.assertAlmostEqual(advertising["age"], 67.0)

        aerospace = next(
            item
            for item in data
            if item["industry"]
            == "Aerospace"
            )
        self.assertAlmostEqual(aerospace["age"], 94.0)

        agricultural_chemicals = next(
            item
            for item in data
            if item["industry"]
            == "Agricultural Chemicals"
        )
        self.assertAlmostEqual(agricultural_chemicals["age"], 54.0)

        air_freight_delivery_services = next(
            item
            for item in data
            if item["industry"]
            == "Air Freight/Delivery Services"
        )
        self.assertAlmostEqual(air_freight_delivery_services["age"], 43.0)

        apparel = next(item for item in data if item["industry"] == "Apparel")
        self.assertAlmostEqual(apparel["age"], 64.0)

        auto_manufacturing = next(
            item for item in data if item["industry"] == "Auto Manufacturing"
        )
        self.assertAlmostEqual(auto_manufacturing["age"], 32.0)

        auto_parts_oem = next(
            item for item in data if item["industry"] == "Auto Parts:O.E.M."
        )
        self.assertAlmostEqual(auto_parts_oem["age"], 49.0)

        automotive_aftermarket = next(
            item
            for item in data
            if item["industry"]
            == "Automotive Aftermarket"
        )
        self.assertAlmostEqual(automotive_aftermarket["age"], 42.0)

        banks = next(item for item in data if item["industry"] == "Banks")
        self.assertAlmostEqual(banks["age"], 56.8)

        biotechnology_biological_products = next(
            item
            for item in data
            if item["industry"]
            == "Biotechnology: Biological Products (No Diagnostic Substances)"
        )
        self.assertAlmostEqual(
            biotechnology_biological_products["age"],
            32.333333333333336
        )

        # test_average_salary_per_industry
        response = self.client.get(reverse("average-salary-per-industry"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assertions to check response data for average_salary_per_industry
        data = response.json()

        advertising = next(
            item for item in data if
            item["industry"] == "Advertising"
            )
        self.assertAlmostEqual(
            advertising["salary"],
            86958.24
            )

        aerospace = next(
            item for item in data if
            item["industry"] == "Aerospace"
                         )
        self.assertAlmostEqual(
            aerospace["salary"],
            1000.0
            )

        agricultural_chemicals = next(
            item for item in data if item["industry"] ==
            "Agricultural Chemicals"
        )
        self.assertAlmostEqual(
            agricultural_chemicals["salary"],
            155098.84
            )

        air_freight_delivery_services = next(
            item for item in data if item["industry"] ==
            "Air Freight/Delivery Services"
        )
        self.assertAlmostEqual(
            air_freight_delivery_services["salary"],
            180357.63
            )

        apparel = next(item for item in data if item["industry"] == "Apparel")
        self.assertAlmostEqual(
            apparel["salary"],
            156957.58333333334
            )

        auto_manufacturing = next(
            item for item in data if item["industry"] == "Auto Manufacturing"
        )
        self.assertAlmostEqual(
            auto_manufacturing["salary"],
            78859.77
            )

        auto_parts_oem = next(
            item for item in data if item["industry"] == "Auto Parts:O.E.M."
        )
        self.assertAlmostEqual(
            auto_parts_oem["salary"],
            165628.86
            )

        automotive_aftermarket = next(
            item for item in data if item["industry"] ==
            "Automotive Aftermarket"
        )
        self.assertAlmostEqual(
            automotive_aftermarket["salary"],
            124827.03333333334
            )

        banks = next(item for item in data if item["industry"] == "Banks")
        self.assertAlmostEqual(banks["salary"], 150870.984)

        biotechnology_biological_products = next(
            item
            for item in data
            if item["industry"]
            == "Biotechnology: Biological Products (No Diagnostic Substances)"
        )
        self.assertAlmostEqual(
            biotechnology_biological_products["salary"],
            171342.06666666668
        )

        # test_average_salary_per_experience
        response = self.client.get(reverse("average-salary-per-experience"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assertions to check response data for average_salary_per_experience
        data = response.json()

        two_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 2
        )
        self.assertAlmostEqual(
            two_years_of_experience["salary"],
            148298.93357142858
            )

        three_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 3
        )
        self.assertAlmostEqual(
            three_years_of_experience["salary"],
            115574.91
            )

        four_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 4
        )
        self.assertAlmostEqual(
            four_years_of_experience["salary"],
            157010.267
            )

        five_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 5
        )
        self.assertAlmostEqual(
            five_years_of_experience["salary"],
            156833.75363636363
            )

        six_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 6
        )
        self.assertAlmostEqual(
            six_years_of_experience["salary"],
            159633.38571428572
            )

        seven_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 7
        )
        self.assertAlmostEqual(
            seven_years_of_experience["salary"],
            147415.14642857143
            )

        eight_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 8
        )
        self.assertAlmostEqual(
            eight_years_of_experience["salary"],
            133680.73666666666
            )

        nine_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 9
        )
        self.assertAlmostEqual(
            nine_years_of_experience["salary"],
            142040.0872222222
            )

        ten_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 10
        )
        self.assertAlmostEqual(
            ten_years_of_experience["salary"],
            155445.87473684212
            )

        eleven_years_of_experience = next(
            item for item in data if item["years_of_experience"] == 11
        )
        self.assertAlmostEqual(
            eleven_years_of_experience["salary"],
            122410.22153846153
            )

        # test_median_salary_per_industry
        response = self.client.get(reverse("median-salary-per-industry"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Add assertions to check response data for median_salary_per_industry
        data = response.json()
        advertising_median_salary = next(
            item for item in data if item["industry"] == "Advertising"
            )
        self.assertAlmostEqual(advertising_median_salary["salary"], 86958.24)

        # test_delete_employees_from_mocked_data
        for employee_data in self.mocked_data:
            response = self.client.delete(
                reverse(
                    "employee-retrieve-update-destroy",
                    kwargs={"pk": employee_data["id"]},
                )
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
