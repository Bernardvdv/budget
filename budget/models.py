from django.db import models
from django.utils.timezone import timedelta
from dateutil.relativedelta import relativedelta


class Period(models.Model):
    # month = models.CharField(max_length=180, unique=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name_plural = "period"

    def __str__(self):
        return self.name

    def duplicate(self):
        new_period = Period.objects.create(
            name=f"{self.name} (Copy)",
            start_date=self.end_date + timedelta(days=1),
            end_date=self.end_date + relativedelta(months=1),
        )
        expenses = self.expenses.all()
        for expense in expenses:
            new_expense = Items.objects.create(
                month=new_period,
                name=expense.name,
                value=expense.value,
                category=expense.category,
                payment_date=expense.payment_date,
                person=expense.person
            )

        return new_period


class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category


class Income(models.Model):
    person = models.CharField(max_length=180, unique=False)
    income_year = models.IntegerField()
    income_month = models.IntegerField()

    class Meta:
        verbose_name_plural = "income"

    def __str__(self):
        return self.person


class Items(models.Model):
    month = models.ForeignKey(Period, related_name='expenses', on_delete=models.CASCADE)
    name = models.CharField(max_length=180)
    value = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    payment_date = models.DateField()
    person = models.ForeignKey(Income, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "items"

    def __str__(self):
        return f'{self.month.name} - {self.name}'


class BaseConfig(models.Model):
    COUNTRIES = [
        ("South Africa", "South Africa"),
        ("United Kingdom", "United Kingdom"),
    ]
    DEFAULT = "United Kingdom"

    name = models.CharField(max_length=100, unique=True)
    currency = models.CharField(max_length=10, unique=True)
    country = models.CharField(
        max_length=50,
        choices=COUNTRIES,
        default=DEFAULT
    )

    class Meta:
        verbose_name_plural = "base config"

    def __str__(self):
        return self.name


class UserSettings(models.Model):
    month = models.CharField(max_length=100, unique=False)

    class Meta:
        verbose_name_plural = "user settings"
