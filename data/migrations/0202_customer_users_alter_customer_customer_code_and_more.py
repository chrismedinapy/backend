# Generated by Django 4.0.2 on 2022-03-01 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0201_remove_customer_users_alter_customer_customer_code_and_more'),
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
            field=models.UUIDField(default='a390660b-0f84-44d6-84e1-39e16320820d', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='46d2ae9b-5181-411f-8353-9b2e044f5e27', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='e6fcef15-d6aa-4fa8-b5cc-87db95d5e352', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='46cf12c7-7a56-4855-a86a-40eb0221f366', primary_key=True, serialize=False),
        ),
    ]