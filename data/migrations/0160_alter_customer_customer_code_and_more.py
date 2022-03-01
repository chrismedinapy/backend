# Generated by Django 4.0.2 on 2022-02-26 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0159_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='38c429ad-d994-40d1-8240-54a393c58018', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='d1b0ad81-a4e8-4318-a50a-92b32b73e529', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='6c56bffd-eb39-4467-9e79-62b440e1646c', primary_key=True, serialize=False),
        ),
    ]