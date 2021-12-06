# Generated by Django 3.2.8 on 2021-12-06 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, verbose_name='Phone Number'),
        ),
    ]
