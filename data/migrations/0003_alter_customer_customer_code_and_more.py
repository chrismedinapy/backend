# Generated by Django 4.0.6 on 2022-08-10 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='659282a3-1625-47cc-94e2-dc3cd026fba1', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='ae32a8bd-9c2f-41e4-a7a2-fddbb18dd5b2', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='a2d69a61-b461-4f28-b786-54d48018c0e8', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='e810ab2f-e65d-421c-8c85-24c2ee15a2f9', primary_key=True, serialize=False),
        ),
    ]
