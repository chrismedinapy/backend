<<<<<<< HEAD
# Generated by Django 4.0.2 on 2022-06-01 15:25
=======
# Generated by Django 4.0.2 on 2022-04-29 18:09
>>>>>>> main

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0031_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
<<<<<<< HEAD
            field=models.UUIDField(default='e6804161-a142-4ddc-bbef-93c0aa30ea60', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='c56e572b-6c63-48f8-95d4-d022ac516783', primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
<<<<<<< HEAD
            field=models.UUIDField(default='d00874c1-3f61-4bda-b4e9-127c1e6f13cd', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='cdac4b9e-234d-4f92-91bf-da3c2fffacc0', primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
<<<<<<< HEAD
            field=models.UUIDField(default='dad0ba11-7033-4034-b7cc-5b933bc35be5', editable=False, primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='5c42819a-032e-4f11-906d-0eab3c0727a0', editable=False, primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
<<<<<<< HEAD
            field=models.UUIDField(default='f19d8d59-238d-4cb2-8d45-09ca27ef997a', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='74655540-5c5b-46f6-a234-6acffb8fe008', primary_key=True, serialize=False),
>>>>>>> main
        ),
    ]
