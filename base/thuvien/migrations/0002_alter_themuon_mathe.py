# Generated by Django 3.2.8 on 2021-11-06 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thuvien', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='themuon',
            name='maThe',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
