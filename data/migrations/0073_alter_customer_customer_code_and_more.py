# Generated by Django 4.0.2 on 2022-02-14 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0072_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='f4603783-9162-419b-80b4-1f971a371b91', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='21276415-af27-44e6-84bc-b241629a9f70', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='69802aa6-abbf-455c-8426-c20d75076437', primary_key=True, serialize=False),
        ),
    ]
