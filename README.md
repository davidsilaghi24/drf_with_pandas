# Employee Statistics API

This project is a simple Django REST API that allows users to create, retrieve, update, and delete employee records. Additionally, the API provides several endpoints to retrieve statistics based on the employee data, such as average age and salary by industry, and average salary by years of experience.

# Features

Employee CRUD (Create, Read, Update, Delete) operations
Pagination for the employee list
Search, ordering, and filtering for the employee list
Average age per industry
Average salary per industry
Average salary per years of experience

# Technologies Used

Python
Django
Django REST framework
PostgreSQL (for database)
drf-spectacular (for API schema generation)

# Installation

Clone the repository

git clone https://github.com/yourusername/employee-statistics-api.git

Build docker and launch it

docker-compose build
docker-compose up

# Usage

The following endpoints are available:

/api/employees/ - List, create, search, order, and filter employees
/api/employees/<int:pk>/ - Retrieve, update, and delete a specific employee
/api/statistics/average-age/ - Get the average age per industry
/api/statistics/average-salary/ - Get the average salary per industry
/api/statistics/average-salary-experience/ - Get the average salary per years of experience

# Testing

To run the tests, execute:

python manage.py test
The tests cover the basic CRUD operations for employees, as well as the statistical endpoints.
