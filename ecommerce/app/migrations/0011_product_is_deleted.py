# Generated by Django 5.2 on 2025-04-29 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_customer_options_alter_customer_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
