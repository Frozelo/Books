# Generated by Django 4.1.5 on 2023-03-23 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_userbookrelation_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbookrelation',
            old_name='book',
            new_name='books',
        ),
    ]
