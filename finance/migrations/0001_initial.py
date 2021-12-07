# Generated by Django 3.2.8 on 2021-12-07 02:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Finance',
                'verbose_name_plural': 'Finances',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('amount', models.IntegerField(verbose_name='Name')),
                ('finance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.finance')),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
            },
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('amount', models.IntegerField(verbose_name='Name')),
                ('finance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.finance')),
            ],
            options={
                'verbose_name': 'Cost',
                'verbose_name_plural': 'Costs',
            },
        ),
    ]
