# Generated by Django 4.0.2 on 2022-02-26 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0158_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='452a9c54-a537-4262-ad3b-40b1a4f99e7d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='b7ec2198-6f66-4e88-812d-03a045972fd2', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='db3c5514-63c3-4eac-82fc-38f96563085d', primary_key=True, serialize=False),
        ),
    ]
