# Generated by Django 4.0.2 on 2022-02-26 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0148_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='55ab0708-3587-4312-944f-58e671737708', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='0881c72e-f085-4606-a426-b122e007f44e', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='ea634e5a-bb4f-4b3e-9619-dbaedb1d78e1', primary_key=True, serialize=False),
        ),
    ]