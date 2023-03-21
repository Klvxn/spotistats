# Generated by Django 4.1.6 on 2023-03-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "artist_id",
                    models.CharField(max_length=15, primary_key=True, serialize=False),
                ),
                ("monthly_listeners", models.CharField(max_length=10)),
            ],
        ),
    ]
