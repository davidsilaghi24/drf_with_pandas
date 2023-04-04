from django.db import models
from datetime import date

class Employee(models.Model):
    unique_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    industry = models.CharField(max_length=255)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    other_fields = models.JSONField(blank=True, null=True)

    @property
    def years_of_experience(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.unique_id}"
