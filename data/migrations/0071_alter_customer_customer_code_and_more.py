# Generated by Django 4.0.2 on 2022-02-14 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0070_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='a866f95a-35bb-4f6e-9980-26badee592ff', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='ff1c9fb0-5d8a-4b34-b63a-0145076bca86', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='3052a1eb-d460-459a-ba52-c6d97606343e', primary_key=True, serialize=False),
        ),
    ]
