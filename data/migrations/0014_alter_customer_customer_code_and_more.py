# Generated by Django 4.0.6 on 2022-09-06 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='ed955f9e-bed0-4ec0-bec8-afcf4ac2f1bc', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='79cdd1a2-a9dd-41b6-8d64-8a865201d68a', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='44393d9c-cd47-4dd5-87bc-0b70b5ea90d9', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='aa02978c-7781-40ef-8f5d-1b8f0ca9b22c', primary_key=True, serialize=False),
        ),
    ]
