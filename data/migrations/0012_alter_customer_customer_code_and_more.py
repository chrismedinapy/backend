# Generated by Django 4.0.6 on 2022-08-11 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='88c94396-36d6-40ea-abe4-d7c9ac2f9ee5', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='f61f4673-7e89-444f-b05b-4b6c7eb510d1', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='bc0240cc-e415-410b-84dd-076b2f4e7c44', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='13f179f7-c09b-4c62-85a4-6258d2fcf5aa', primary_key=True, serialize=False),
        ),
    ]
