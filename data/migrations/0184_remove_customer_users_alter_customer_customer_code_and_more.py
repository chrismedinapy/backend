# Generated by Django 4.0.2 on 2022-02-28 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0183_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='users',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='0cfe326e-0338-4bc9-ad3c-897ef18cfe02', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='8796d122-d803-4919-b02d-76f3cfaa5012', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='c2c8a423-35b4-4229-835e-e0f41cf452a5', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='8b4a5f9d-bb87-4ca0-a96e-4dfd8903a941', primary_key=True, serialize=False),
        ),
    ]
