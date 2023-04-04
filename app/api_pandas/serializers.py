from rest_framework import serializers
from api_pandas.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    class Meta:
        model = Employee
        fields = '__all__'

    def validate_salary(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Annual income must be a positive value.")
        return value
