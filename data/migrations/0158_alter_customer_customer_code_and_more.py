# Generated by Django 4.0.2 on 2022-02-26 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0157_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='8fd3e13c-5cd4-4dc0-956b-79844b32171d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='f19f1ff9-e1ff-4cf6-a83e-339523f9910d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='d8f9efe0-80ea-4d28-bc64-8051b8c650bd', primary_key=True, serialize=False),
        ),
    ]
