<<<<<<< HEAD
# Generated by Django 4.0.2 on 2022-07-18 13:48
=======
# Generated by Django 4.0.4 on 2022-06-21 20:59
>>>>>>> main

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0041_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
<<<<<<< HEAD
            field=models.UUIDField(default='13917cab-6787-48de-952c-94c3c9537905', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='aec11e29-db32-445f-9f88-1e5f11db212a', primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
<<<<<<< HEAD
            field=models.UUIDField(default='c3b95d9c-a57d-431f-8e9a-867a914653a8', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='35d9b111-9645-47f6-a217-2d6ae35a00c5', primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
<<<<<<< HEAD
            field=models.UUIDField(default='a582ba1b-8cc2-4db3-a8f3-0d9972a960ce', editable=False, primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='f7b69aaf-4306-4934-8995-f69198cc27f7', editable=False, primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
<<<<<<< HEAD
            field=models.UUIDField(default='4a2792b2-d22a-4531-907c-85a48fbfeba5', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='7b59933e-0d30-4fa0-8f73-445ec03358c5', primary_key=True, serialize=False),
>>>>>>> main
        ),
    ]
