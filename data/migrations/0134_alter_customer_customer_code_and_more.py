# Generated by Django 4.0.2 on 2022-02-22 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0133_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='3c3d5e8b-9e4f-4fcb-b25f-884b4d7ae8b2', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='61a64e23-5642-4a60-8fdd-ce587111ce7f', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='dad8a014-6abb-4d8c-a175-e74fa4ceecbf', primary_key=True, serialize=False),
        ),
    ]