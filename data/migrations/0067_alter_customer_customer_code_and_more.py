# Generated by Django 4.0.2 on 2022-02-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0066_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='e571c3f6-6f72-480b-9a9e-a8e954144966', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='db5e995f-b4a0-4ccf-a9bd-3e3047a3e5c4', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='8f72c1a9-199d-4d10-838c-424b53026168', primary_key=True, serialize=False),
        ),
    ]