# Generated by Django 4.0.2 on 2022-03-21 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='c344d3d0-1f41-4546-ac89-1b432d6022fa', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='80df65a7-1e97-4637-b4a7-6b43f361a603', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='fee6a947-146a-4e84-8302-e743fee5e64c', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='f53804f6-4ba5-45e2-9050-db85df5b6712', primary_key=True, serialize=False),
        ),
    ]