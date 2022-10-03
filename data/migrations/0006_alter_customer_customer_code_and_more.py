# Generated by Django 4.0.6 on 2022-08-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='f93c21ea-44ec-4f70-b8bc-4bba1878d411', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='20d2fea3-5e33-4073-a7da-5834ab541776', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='8b96b2b6-35f9-4fd8-9899-4ffdb7fbe72f', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='1b5a6985-4e8c-4a01-a16c-19fb5fd2ada6', primary_key=True, serialize=False),
        ),
    ]