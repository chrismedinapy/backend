# Generated by Django 4.0.1 on 2022-02-13 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0037_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='84941ab9-15a5-4224-9771-089e38485341', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='188334ca-2f50-4387-add1-5f277e425236', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='1a81a9a2-3cf2-4199-9e2a-90eaf5fd7b95', primary_key=True, serialize=False),
        ),
    ]
