<<<<<<< HEAD
# Generated by Django 4.0.2 on 2022-07-15 11:49
=======
# Generated by Django 4.0.2 on 2022-06-15 18:25
>>>>>>> main

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0037_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
<<<<<<< HEAD
            field=models.UUIDField(default='a54dc343-be46-48c1-a64d-3d718f791247', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='2d3ce947-570e-4330-8a80-4e63e34a3b03', primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
<<<<<<< HEAD
            field=models.UUIDField(default='c8e60c42-dae3-45c3-bb4d-703f090d5d4a', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='115b7c36-5389-4783-8a74-0895cfaa14e0', primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
<<<<<<< HEAD
            field=models.UUIDField(default='3d04929f-9da6-4c07-8ba6-a5a78a037712', editable=False, primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='930094fc-4383-4686-9cbc-15c9659e9c47', editable=False, primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
<<<<<<< HEAD
            field=models.UUIDField(default='0c02dde5-d5d4-4d03-892b-78ebb6267fec', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='bb5b9d93-71a5-41d5-b968-375d06c5982f', primary_key=True, serialize=False),
>>>>>>> main
        ),
    ]
