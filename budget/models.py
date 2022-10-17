from django.db import models


class Items(models.Model):
    DEFAULT = "Home"
    CATEGORIES = [
        ("Home", "Home"),
        ("School", "School"),
        ("Utility", "Utilities"),
        ("Groceries", "Groceries"),
        ("Mobile", "Mobile"),
        ("Subscriptions", "Subscriptions"),
        ('Car', "Car"),
        ("Other", "Other"),
    ]
    PERSON = [
        ("Bernard", "Bernard"),
        ("Tania", "Tania"),
    ]
    name = models.CharField(max_length=180, unique=True)
    value = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORIES, default=DEFAULT)
    payment_date = models.DateField()
    person = models.CharField(max_length=20, choices=PERSON)


    def __str__(self):
        return self.name


class Income(models.Model):
    person = models.CharField(max_length=180, unique=False)
    income_year = models.CharField(max_length=180, unique=False)
    income_month = models.CharField(max_length=180, unique=False)

    def __str__(self):
        return self.person


class BaseConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    currency = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

