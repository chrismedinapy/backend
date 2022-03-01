# Generated by Django 4.0.2 on 2022-03-01 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0200_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='users',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='e0f1d469-2441-4761-a780-25e6e4bae1dd', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='ca8edd1a-157b-4304-a62e-8df70ab6acd6', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='7109285a-b59d-49c3-b5b5-35eca399c26e', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='adf522f3-ae81-4b2f-a9fc-c19af71ad67a', primary_key=True, serialize=False),
        ),
    ]