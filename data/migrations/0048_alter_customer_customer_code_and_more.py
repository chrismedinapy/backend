# Generated by Django 4.0.2 on 2022-02-14 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0047_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='50db95c7-acb6-440d-96a0-097e8550e745', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='b25ab07c-65fa-4289-b445-86b3ba437d7b', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='2c34c5b6-11d8-4b08-a4ea-37feb6a84ee9', primary_key=True, serialize=False),
        ),
    ]
