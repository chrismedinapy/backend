# Generated by Django 4.0.2 on 2022-03-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='b59d9c86-e697-4a62-968a-9b4bfed3de43', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='8c089591-0a5d-4507-ba6b-a24700aba170', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='c5611ef1-a1c7-47d7-97b2-28f03a578f55', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='2663ea6a-7c44-4da8-b7c7-847cea103d46', primary_key=True, serialize=False),
        ),
    ]