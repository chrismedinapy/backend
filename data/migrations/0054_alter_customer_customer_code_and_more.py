# Generated by Django 4.0.2 on 2022-02-14 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0053_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='1008a631-795c-4f72-b45a-cbb33a7509ad', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='18cdb3c8-ee2d-47b0-ad7a-7b6f8f3541e0', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='0a3ab852-ac76-4242-bfa5-f307831a06aa', primary_key=True, serialize=False),
        ),
    ]
