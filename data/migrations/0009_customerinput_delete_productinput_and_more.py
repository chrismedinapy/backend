# Generated by Django 4.0.1 on 2022-02-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_alter_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInput',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uptated_at', models.DateTimeField(auto_now=True)),
                ('customer_input_code', models.UUIDField(default='682d3989-dd32-4992-acb0-59eb8c30ff32', primary_key=True, serialize=False)),
                ('customer_input_name', models.CharField(max_length=500)),
                ('status', models.IntegerField()),
                ('customer_input_description', models.CharField(max_length=500)),
                ('cvs_location', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='ProductInput',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.UUIDField(default='038a91ef-1f97-4809-9eb8-e2e35f29f111', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.UUIDField(default='edadbd9d-8dc4-4e61-8ccc-cd313ed6398a', primary_key=True, serialize=False),
        ),
    ]