from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from api_pandas.models import Employee
from api_pandas.serializers import EmployeeSerializer
import pandas as pd


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class EmployeeListCreate(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend
        ]
    search_fields = ['first_name', 'last_name', 'industry']
    ordering_fields = [
        'first_name', 'last_name', 'industry', 'date_of_birth', 'annual_income'
        ]
    filterset_fields = ['industry']
    pagination_class = CustomPagination


class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


def get_employee_dataframe():
    queryset = Employee.objects.all()
    serializer = EmployeeSerializer(queryset, many=True)
    return pd.DataFrame(serializer.data)


@api_view(['GET'])
def average_age_per_industry(request):
    df = get_employee_dataframe()
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    df['age'] = (pd.Timestamp.now() - df['date_of_birth']).dt.days // 365
    result = df.groupby('industry')['age'].mean().reset_index()
    return Response(result.to_dict(orient='records'))


@api_view(['GET'])
def average_salary_per_industry(request):
    df = get_employee_dataframe()
    df['salary'] = pd.to_numeric(df['salary'])
    result = df.groupby('industry')['salary'].mean().reset_index()
    return Response(result.to_dict(orient='records'))


@api_view(['GET'])
def average_salary_per_experience(request):
    df = get_employee_dataframe()
    df['years_of_experience'] = pd.to_numeric(df['years_of_experience'])
    df['salary'] = pd.to_numeric(df['salary'])
    result = df.groupby('years_of_experience')['salary'].mean().reset_index()
    return Response(result.to_dict(orient='records'))


# interesting statistics
@api_view(['GET'])
def median_salary_per_industry(request):
    df = get_employee_dataframe()
    df['salary'] = pd.to_numeric(df['salary'])
    result = df.groupby('industry')['salary'].median().reset_index()
    return Response(result.to_dict(orient='records'))
