# Generated by Django 4.0.2 on 2022-02-26 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0153_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='3e8f42c6-6553-4641-83e3-b6be1704728c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='23b112ab-360a-4c01-8844-b10e800622dd', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='13060f4b-24bc-4b82-8093-d0e6587f2fdd', primary_key=True, serialize=False),
        ),
    ]