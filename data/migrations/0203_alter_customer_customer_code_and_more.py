# Generated by Django 4.0.2 on 2022-03-01 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0202_customer_users_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='cf07b565-9e9d-4583-8e14-9d4fc542105c', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerinput',
            name='customer_input_code',
            field=models.UUIDField(default='7a5d55b8-99ed-4c65-a29b-cb555c5c8550', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer',
            field=models.ForeignKey(blank=True, db_column='membership_customer', null=True, on_delete=django.db.models.deletion.CASCADE, to='data.customer'),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='customer_user_group_code',
            field=models.UUIDField(default='cdc73ba6-491f-4ee0-8c0b-86b001228ebc', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customerusergroup',
            name='user',
            field=models.ForeignKey(blank=True, db_column='membership_user', null=True, on_delete=django.db.models.deletion.CASCADE, to='data.user'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='7fb40c9a-8507-4498-93e8-6f36e3cba7fe', primary_key=True, serialize=False),
        ),
    ]
