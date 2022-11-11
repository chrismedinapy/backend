# Generated by Django 4.0.7 on 2022-11-11 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0024_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='a3c78a41-0c4c-414a-8181-15451d12d251', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='01919ef5-b200-4b3f-bbff-1c349aa50605', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='160e9763-561a-46a8-bc1d-ddfa6df8a28a', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='7a1e884d-5750-4ff1-9c30-582d31a5814c', primary_key=True, serialize=False),
        ),
    ]
