# Generated by Django 4.0.2 on 2022-02-15 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0079_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='d61b66ce-936b-4eea-9a32-c955746eae20', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='9f714675-e4fd-4d71-a8ed-3616db8cf76d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='5251ffca-9704-4ebe-b554-d33ddeb69c7d', primary_key=True, serialize=False),
        ),
    ]
