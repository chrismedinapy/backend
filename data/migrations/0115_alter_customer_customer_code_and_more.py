# Generated by Django 4.0.2 on 2022-02-16 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0114_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='b8d7e486-7a61-4e2a-8236-740219d7a04c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='d3d01ff9-a2a1-4218-b71a-48bfb621b8e5', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='1adee2d2-db4f-42c0-b464-39293d5fac8f', primary_key=True, serialize=False),
        ),
    ]