# Generated by Django 3.2.8 on 2021-12-09 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20211209_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='names',
            field=models.CharField(max_length=255, verbose_name='Profile names'),
        ),
    ]
