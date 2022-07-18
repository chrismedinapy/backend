# Generated by Django 4.0.2 on 2022-05-17 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0027_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='787fbfbb-04e5-4e2b-963f-0d11d500b322', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='97be0f83-7b83-4016-8ca2-4215d6fe145d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='e86b5816-dd6c-4ddb-bc84-5b044a359b46', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='ba1437ef-10a7-4d30-b803-a8e8c1a86562', primary_key=True, serialize=False),
        ),
    ]
