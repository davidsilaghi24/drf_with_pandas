from rest_framework import serializers
from api_pandas.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_annual_income(self, value):
        if value < 0:
            raise serializers.ValidationError("Annual income must be a positive value.")
        return value
