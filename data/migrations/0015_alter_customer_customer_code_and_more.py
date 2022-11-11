# Generated by Django 4.0.6 on 2022-09-06 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='cd92a10c-ef10-405e-a164-6cf17f05812f', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='000d01d4-b6d5-4b30-a413-ee40f123eef3', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='5771ed39-5937-402f-b5c8-8d8ab2db8b82', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='5f330f29-f9f7-432d-a37f-3abe949bf1bd', primary_key=True, serialize=False),
        ),
    ]
