# Generated by Django 4.0.6 on 2022-08-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='541ec2a3-e692-4b6d-98e7-6a4cd426d389', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='295aaeec-ee87-46ed-99e8-410a76dca52c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='1b850e5a-6085-463c-965d-e98b407645f1', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='72e5b626-b02f-4adf-9a94-b9a3d3b60a48', primary_key=True, serialize=False),
        ),
    ]