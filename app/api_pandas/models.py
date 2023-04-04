from django.db import models
from datetime import date

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    industry = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)

    other_fields = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.id}"

    class Meta:
        ordering = ['id']