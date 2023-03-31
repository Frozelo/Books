# Generated by Django 4.1.5 on 2023-03-19 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0007_books_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('in_bookmarks', models.BooleanField(default=False)),
                ('rate', models.PositiveIntegerField(choices=[(1, 'Ok'), (2, 'Good'), (3, 'Amazing'), (4, 'Incredible'), (5, 'Awesome')])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.books')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]