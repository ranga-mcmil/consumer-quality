# Generated by Django 5.1.6 on 2025-02-26 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_review_user_review_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='name',
            new_name='reviewer',
        ),
    ]
