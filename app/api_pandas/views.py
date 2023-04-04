from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api_pandas.models import Employee
from api_pandas.serializers import EmployeeSerializer
import pandas as pd

class EmployeeListCreate(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

@api_view(['GET'])
def average_age_per_industry(request):
    queryset = Employee.objects.values('industry').annotate(avg_age=pd.Timestamp.now().year - pd.to_datetime(pd.DataFrame(Employee.objects.values('dob')).dob).dt.year.mean())
    return Response(queryset)

@api_view(['GET'])
def average_salary_per_industry(request):
    queryset = Employee.objects.values('industry').annotate(avg_salary=pd.Series(Employee.objects.values_list('annual_income', flat=True)).mean())
    return Response(queryset)

@api_view(['GET'])
def average_salary_per_experience(request):
    queryset = Employee.objects.values('years_of_experience').annotate(avg_salary=pd.Series(Employee.objects.values_list('annual_income', flat=True)).mean())
    return Response(queryset)
