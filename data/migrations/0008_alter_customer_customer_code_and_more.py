# Generated by Django 4.0.2 on 2022-03-21 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_customerinput_retail_store_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='b1c14673-57d2-4a5c-91a0-b99c622b61d1', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='ebc7af64-7381-47a7-b0d7-de6bff328c02', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='b2d331e1-24e4-4b58-b57f-8bb29612bade', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='01cae162-0477-4dbc-886d-14f4473fa03d', primary_key=True, serialize=False),
        ),
    ]
