# Generated by Django 4.0.1 on 2022-02-09 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='6ee9b805-8a06-4693-9599-2eaa8fc7cf4a', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='35b85fcb-ffe0-41dc-afdd-1c2345a8038b', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='47185c7a-cb92-4d31-8bf4-d2a61d70b53d', primary_key=True, serialize=False),
        ),
    ]
