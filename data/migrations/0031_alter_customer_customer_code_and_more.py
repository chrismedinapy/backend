# Generated by Django 4.0.2 on 2022-05-31 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0030_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='5cda703c-9093-4e73-89ad-2967b43fd088', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='5de01455-ac55-417b-a836-6ecea9dcfb7b', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='2c5f7f2e-9d7d-4fba-85db-b092919ca040', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='cee579e0-7129-4881-9b3b-3e4630eb0f75', primary_key=True, serialize=False),
        ),
    ]
