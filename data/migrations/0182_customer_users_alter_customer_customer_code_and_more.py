# Generated by Django 4.0.2 on 2022-02-28 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0181_remove_customer_users_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='users',
            field=models.ManyToManyField(through='data.CustomerUserGroup', to='data.User'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='6e5b47d9-f4bd-4383-a53d-4f92fe66f5c6', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='50999b94-1fb2-49bc-9b93-4201e9828b1c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='bc54aa81-0d6f-4e6f-ba69-0584162c5caa', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='ea20d238-00ff-4b48-b9de-fdac003e9dc9', primary_key=True, serialize=False),
        ),
    ]