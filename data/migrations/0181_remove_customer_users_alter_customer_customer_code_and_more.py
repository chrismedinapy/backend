# Generated by Django 4.0.2 on 2022-02-28 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0180_customer_users_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='users',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='c8799264-fb59-445f-b767-a269dfecf1ae', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='b5f66f48-7e42-48a7-ae03-f7eb385e0327', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='03e495a5-d0cb-4d57-bc1e-34b4cda6ee9f', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='ae9f94cc-2633-41e9-8bd4-aa03ae87cb20', primary_key=True, serialize=False),
        ),
    ]
