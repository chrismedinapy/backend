# Generated by Django 4.0.2 on 2022-02-27 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0161_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='09877b42-129a-4951-9502-0748dd757ef8', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='21dca377-30a4-4534-a864-6028e550652c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='13ab027e-1e45-4ec9-8bf3-5073245c01d1', primary_key=True, serialize=False),
        ),
    ]