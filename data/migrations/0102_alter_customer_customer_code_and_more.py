# Generated by Django 4.0.2 on 2022-02-15 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0101_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='d9c62af6-5292-4b91-9a30-ee1710fb33b4', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='51f64e60-cda2-4055-9e25-234a6757dd9d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='e4912b4a-9408-4e6b-8113-8a6ae1473197', primary_key=True, serialize=False),
        ),
    ]