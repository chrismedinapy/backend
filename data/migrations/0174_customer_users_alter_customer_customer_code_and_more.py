# Generated by Django 4.0.2 on 2022-02-28 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0173_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='users',
            field=models.ManyToManyField(blank=True, through='data.CustomerUserGroup', to='data.User'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='9c2100e5-fb47-4666-88d7-9daf8be621cb', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='507c31e1-7ea3-4754-a661-2ca22ea50a65', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='d4e919d0-80d0-4def-8dc1-1e164d301054', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='e1c7eefd-36f3-4e1f-82bf-f56caaff0495', primary_key=True, serialize=False),
        ),
    ]