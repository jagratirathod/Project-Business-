# Generated by Django 3.1.6 on 2022-01-12 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_bidding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='file2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='file3',
        ),
        migrations.RemoveField(
            model_name='product',
            name='file4',
        ),
    ]
