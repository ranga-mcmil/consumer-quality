# Generated by Django 5.1.6 on 2025-02-26 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='review',
            name='name',
            field=models.CharField(default='John Doe', max_length=255),
            preserve_default=False,
        ),
    ]
