# Generated by Django 4.0.2 on 2022-07-11 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0035_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='07ddbf52-893a-4eb6-82e0-593e33ce9ae4', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='3ce2c918-27b8-422c-ae95-24777e980154', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='78236651-66f8-458e-9939-f4c93aff38e8', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='b025d289-4041-4702-8874-2b9f605800a5', primary_key=True, serialize=False),
        ),
    ]
