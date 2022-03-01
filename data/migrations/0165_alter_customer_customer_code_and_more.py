# Generated by Django 4.0.2 on 2022-02-27 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0164_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='0d1d32d4-04c7-40cb-b8a1-11d73b4449bb', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='566a8eed-d815-408d-85ad-b52cc66a57a7', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='cf28a039-1d9d-457a-bfcb-b0e8449b32e2', primary_key=True, serialize=False),
        ),
    ]
