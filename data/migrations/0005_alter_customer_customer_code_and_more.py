# Generated by Django 4.0.6 on 2022-08-10 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='415ab83c-beda-4612-8490-c4495b27fc9f', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='3567be86-6cd2-4162-bfd2-96f2800b0467', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='4ca4aca6-7933-49a4-b94e-690c4d8f914f', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='f838684a-4764-49bc-87d9-b0e08df75359', primary_key=True, serialize=False),
        ),
    ]
