# Generated by Django 4.0.2 on 2022-02-17 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0120_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='11dba94f-34f3-4bc2-9e50-8375187d8f0b', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='920b259c-d84b-4995-85c2-c743321d697e', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='e6b31bf5-1f87-42ed-a5eb-bb2c9952bb99', primary_key=True, serialize=False),
        ),
    ]