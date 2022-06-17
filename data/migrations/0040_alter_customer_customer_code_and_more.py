# Generated by Django 4.0.2 on 2022-06-17 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0039_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='f2dbbbf0-1486-44dd-bfd8-ac38261e479c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='265665f4-afdf-4973-aad6-4959717b6747', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='bcb4d578-6bdb-44b4-a548-ab4ed496b10b', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='7152fa72-9d8a-459e-8864-d35b6d7e3fe8', primary_key=True, serialize=False),
        ),
    ]
