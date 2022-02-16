# Generated by Django 4.0.1 on 2022-02-13 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0042_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='eaf557cd-1d39-42d6-8c16-eb1bf511c45a', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='6aaafd85-50bc-4851-9a7b-67ebb72e1155', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='11cdd2cc-907d-4773-8637-841df9747168', primary_key=True, serialize=False),
        ),
    ]
