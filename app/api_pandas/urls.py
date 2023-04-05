from django.urls import path
from api_pandas.views import (
    EmployeeListCreate,
    EmployeeRetrieveUpdateDestroy,
    average_age_per_industry,
    average_salary_per_industry,
    average_salary_per_experience,
    median_salary_per_industry,
    percentage_of_employees_per_industry
)

urlpatterns = [
    path(
        "employees/",
        EmployeeListCreate.as_view(),
        name="employee-list-create",
    ),
    path(
        "employees/<int:pk>/",
        EmployeeRetrieveUpdateDestroy.as_view(),
        name="employee-retrieve-update-destroy",
    ),
    path(
        "statistics/average-age/",
        average_age_per_industry,
        name="average-age-per-industry",
    ),
    path(
        "statistics/average-salary/",
        average_salary_per_industry,
        name="average-salary-per-industry",
    ),
    path(
        "statistics/average-salary-experience/",
        average_salary_per_experience,
        name="average-salary-per-experience",
    ),
    path(
        "statistics/median-salary/",
        median_salary_per_industry,
        name="median-salary-per-industry",
    ),
    path(
        "statistics/percentage-employees/",
        percentage_of_employees_per_industry,
        name="percentage-employees-per-industry",
     )
]
