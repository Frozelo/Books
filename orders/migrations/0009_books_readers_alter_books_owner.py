# Generated by Django 4.1.5 on 2023-03-19 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0008_userbookrelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='readers',
            field=models.ManyToManyField(related_name='books', through='orders.UserBookRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='books',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_book', to=settings.AUTH_USER_MODEL),
        ),
    ]