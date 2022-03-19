# Generated by Django 4.0.3 on 2022-03-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_category_name_alter_item_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('-date_created', 'price')},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]