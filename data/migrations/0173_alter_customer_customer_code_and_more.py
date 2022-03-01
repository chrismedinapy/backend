# Generated by Django 4.0.2 on 2022-02-27 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0172_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='ab712920-2c73-4c2a-8ddd-e44eb94def1b', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='86e0f0a6-926b-479d-ab7a-cd416e6aa34c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='7ecb1d6a-bb66-4397-ab36-598b5ea0117c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='06ab1a7c-c8c5-4f3e-8719-9d01fa0e86e6', primary_key=True, serialize=False),
        ),
    ]
