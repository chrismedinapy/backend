# Generated by Django 4.0.2 on 2022-02-15 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0083_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='caec979c-9e50-496a-9908-521a91a35617', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='75cdc166-b4d5-47e3-a528-13a896f6496f', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='44216241-1c31-4da0-b159-e038d4c439e0', primary_key=True, serialize=False),
        ),
    ]
