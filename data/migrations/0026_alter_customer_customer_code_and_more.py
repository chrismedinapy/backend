<<<<<<< HEAD
# Generated by Django 4.0.2 on 2022-05-16 22:33
=======
# Generated by Django 4.0.2 on 2022-04-29 13:19
>>>>>>> main

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0025_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
<<<<<<< HEAD
            field=models.UUIDField(default='4d68b4a2-76a3-4a85-99dc-171b068c4480', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='307cb0d8-74c6-4cda-a39a-c806cf6e8cb9', primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
<<<<<<< HEAD
            field=models.UUIDField(default='20f10bc6-ac24-427e-8062-f7ea929e9dce', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='7c0153f7-ec90-4f59-a8cc-0ba058a6b58b', primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
<<<<<<< HEAD
            field=models.UUIDField(default='f7ca86fb-5879-4d63-a797-3c2eb7df96c9', editable=False, primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='4f0d7173-fbc3-489b-b951-10bf59e64597', editable=False, primary_key=True, serialize=False),
>>>>>>> main
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
<<<<<<< HEAD
            field=models.UUIDField(default='699833c7-302c-47b6-be55-86d2cc5ef268', primary_key=True, serialize=False),
=======
            field=models.UUIDField(default='355c6e87-3aed-4515-855a-73038ac93dc5', primary_key=True, serialize=False),
>>>>>>> main
        ),
    ]
