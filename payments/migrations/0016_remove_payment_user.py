# Generated by Django 4.0.3 on 2022-03-19 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0015_alter_coupon_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
    ]
