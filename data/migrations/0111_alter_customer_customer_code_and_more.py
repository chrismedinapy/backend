# Generated by Django 4.0.2 on 2022-02-16 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0110_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='3462cc22-82ac-4d42-8284-f3a9c4baf2f4', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='2edbb7e8-0c61-40e9-938e-165c490ec710', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='81f37267-f599-4a72-bb43-b0562b38771c', primary_key=True, serialize=False),
        ),
    ]
