# Generated by Django 4.1.5 on 2023-03-03 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_books_author_delete_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.CharField(max_length=255),
        ),
    ]
