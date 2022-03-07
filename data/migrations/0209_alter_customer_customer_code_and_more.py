# Generated by Django 4.0.2 on 2022-03-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0208_customer_users_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='d22e3ba0-0a7e-481c-8629-927b26602068', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='1dbcbb88-2df0-42a5-b24a-e12fe1081bf0', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='cfc1dfde-70b0-4fc5-89b1-c0bbb832520f', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='db4b8a2e-571b-435e-892b-3d85f91282f4', primary_key=True, serialize=False),
        ),
    ]