# Generated by Django 4.0.2 on 2022-02-14 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0055_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='44dc474a-7e3c-47e7-b8a8-56555d36930d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='4011dc9b-f63e-4a83-857f-c12a4874e5ac', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='2400bc16-8df8-4f36-8bfe-a0c18ae15e20', primary_key=True, serialize=False),
        ),
    ]