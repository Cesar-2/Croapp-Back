# Generated by Django 3.2.8 on 2021-12-07 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20211207_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='amount_expense',
            field=models.IntegerField(default=0, verbose_name='Expense'),
        ),
    ]