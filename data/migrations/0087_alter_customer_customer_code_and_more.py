# Generated by Django 4.0.2 on 2022-02-15 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0086_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='bd489256-9671-466a-ad67-20293b32e4b6', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='b225d75f-bd21-4ae8-a570-f5c2955a279e', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='93a47271-30cd-41a3-b28b-6f65c4f678e4', primary_key=True, serialize=False),
        ),
    ]
