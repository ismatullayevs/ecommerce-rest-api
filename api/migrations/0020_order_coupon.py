# Generated by Django 4.0.3 on 2022-03-13 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_alter_payment_amount'),
        ('api', '0019_order_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.coupon'),
        ),
    ]