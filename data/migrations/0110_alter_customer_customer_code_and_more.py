# Generated by Django 4.0.2 on 2022-02-16 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0109_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='f02320b8-1be4-4bfa-bfcb-1f5c82a1e741', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='c40555f4-5339-4a16-a15a-cfae4a51280e', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='8865c31f-b5d9-4227-9671-df3713dd6349', primary_key=True, serialize=False),
        ),
    ]