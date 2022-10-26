from django.db import models


class Period(models.Model):
    month = models.CharField(max_length=180, unique=True)

    class Meta:
        verbose_name_plural = "period"

    def __str__(self):
        return self.month


# class Category(models.Model):
#     DEFAULT = "Home"
#     CATEGORIES = [
#         ("Home", "Home"),
#         ("School", "School"),
#         ("Utility", "Utilities"),
#         ("Groceries", "Groceries"),
#         ("Mobile", "Mobile"),
#         ("Subscriptions", "Subscriptions"),
#         ('Car', "Car"),
#         ("Other", "Other"),
#     ]
#
#     # month = models.ForeignKey(Period, on_delete=models.CASCADE)
#     category = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.category

class Income(models.Model):
    person = models.CharField(max_length=180, unique=False)
    income_year = models.IntegerField()
    income_month = models.IntegerField()

    class Meta:
        verbose_name_plural = "income"

    def __str__(self):
        return self.person


class Items(models.Model):
    DEFAULT = "Home"
    CATEGORIES = [
        ("Home", "Home"),
        ("School", "School"),
        ("Utility", "Utilities"),
        ("Groceries", "Groceries"),
        ("Data", "Data"),
        ("Subscriptions", "Subscriptions"),
        ('Car', "Car"),
        ("Other", "Other"),
    ]

    class Meta:
        verbose_name_plural = "items"

    month = models.ForeignKey(Period, on_delete=models.CASCADE)
    name = models.CharField(max_length=180, unique=True)
    value = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORIES,
                                default=DEFAULT)
    payment_date = models.DateField()
    person = models.ForeignKey(Income, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.month.month} - {self.name}'


class BaseConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    currency = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "base config"

    def __str__(self):
        return self.name


class UserSettings(models.Model):
    month = models.CharField(max_length=100, unique=False)

    class Meta:
        verbose_name_plural = "user settings"
