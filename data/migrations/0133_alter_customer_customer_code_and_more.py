# Generated by Django 4.0.2 on 2022-02-22 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0132_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='87b711b8-395a-4063-afd8-a91a766ba705', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='f3e2b18c-a80e-419a-b378-4ca8fb62db77', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='8ddc36c3-c4e2-404d-b42c-47829254ffc3', primary_key=True, serialize=False),
        ),
    ]
