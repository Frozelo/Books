# Generated by Django 4.1.5 on 2023-03-31 13:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0013_books_rating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userbookrelation',
            unique_together={('user', 'book')},
        ),
    ]
