from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Finance(models.Model):
    name = models.CharField("Name", max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Finance"
        verbose_name_plural = "Finances"

    def __str__(self):
        return self.name


class Cost(models.Model):
    name = models.CharField("Name", max_length=100)
    amount = models.IntegerField("Name")
    finance = models.ForeignKey(Finance, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cost"
        verbose_name_plural = "Costs"

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField("Name", max_length=100)
    amount = models.IntegerField("Name")
    finance = models.ForeignKey(Finance, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    def __str__(self):
        return self.name
