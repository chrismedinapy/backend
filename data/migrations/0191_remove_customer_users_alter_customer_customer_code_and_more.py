# Generated by Django 4.0.2 on 2022-03-01 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0190_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='users',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='5bbeede9-8b2b-41b7-944f-80c5e18abbf1', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='24563205-20ec-4163-8683-2c9897b4f0ad', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='34afeb50-a022-463e-8d6e-81b2608737e8', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='37c8b99d-4d25-4331-985c-e53ce62bfdcd', primary_key=True, serialize=False),
        ),
    ]
