from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'unique_id',
            'first_name',
            'last_name',
            'date_of_birth',
            'industry',
            'annual_income',
            'years_of_experience',
            'other_fields'
        )
