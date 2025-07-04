# Generated by Django 5.2 on 2025-04-29 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_product_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['title'], name='title_index'),
        ),
    ]
