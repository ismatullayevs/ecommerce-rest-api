# Generated by Django 4.0.3 on 2022-03-11 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_order_address_alter_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=3),
        ),
    ]
