# Generated by Django 4.0.2 on 2022-05-17 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0026_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='ba4ea07d-4067-4643-8f81-100e12f64ca4', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='90a59a84-c428-4c1a-b901-3899d09f70eb', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='cda5e6ae-b188-45a7-ba1d-3fe5ee45cd09', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='3815d98b-afc6-4868-84c1-11fa53760fc1', primary_key=True, serialize=False),
        ),
    ]
