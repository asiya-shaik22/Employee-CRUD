from django.core.validators import MinValueValidator
from django.db import models


class Employee(models.Model):
    joining_date = models.DateField()
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    education = models.CharField(max_length=20)
    skills = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    experience = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return self.name
