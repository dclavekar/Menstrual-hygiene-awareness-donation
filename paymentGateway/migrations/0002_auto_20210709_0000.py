# Generated by Django 3.1 on 2021-07-08 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paymentGateway', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donate',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='donate',
            name='phone',
        ),
    ]