# Generated by Django 4.0.2 on 2022-02-26 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0135_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='5cc7544e-d58a-4069-ae03-efe778a46924', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='73f374d1-6a72-41e8-9cbb-c1d2dd9fe041', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='f877b625-cbcb-4aef-9fe1-30b0c8a76490', primary_key=True, serialize=False),
        ),
    ]