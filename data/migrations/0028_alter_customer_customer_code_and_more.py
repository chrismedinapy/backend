# Generated by Django 4.0.2 on 2022-04-29 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0027_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='f1c17a76-9eba-41e5-925a-591893cc9f58', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='a156ad8a-de95-4863-8fca-4b92e692e40e', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='dcb5b418-d7f8-43b1-aeec-6360646ad077', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='874c1f91-04ec-408a-ba86-a475b93683ec', primary_key=True, serialize=False),
        ),
    ]
