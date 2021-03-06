# Generated by Django 4.0.4 on 2022-07-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0050_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='63a8906b-0543-4e9f-a590-f2ad2c417765', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='96ad2f35-7496-4b7a-9227-48a9f6727f3d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='f5905040-2812-41ae-adc4-66df6de0441c', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='94466bc7-dc47-4461-b575-b7fca296323d', primary_key=True, serialize=False),
        ),
    ]
