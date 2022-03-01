# Generated by Django 4.0.2 on 2022-03-01 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0185_customer_users_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='7ca046eb-9f7b-4c2f-a10d-62cdbe5e7501', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='57cf30e3-8560-4887-829a-9b48bab8d0d1', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='6f45b3a8-9c21-43b3-b5b2-98732616ce1e', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='23690dce-8d1e-401b-b6db-253932065619', primary_key=True, serialize=False),
        ),
    ]