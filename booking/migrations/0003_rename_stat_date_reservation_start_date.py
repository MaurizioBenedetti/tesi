# Generated by Django 5.1.5 on 2025-01-19 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_rename_hotel_front_picture_hotel_hotel_front_picture_url_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='stat_date',
            new_name='start_date',
        ),
    ]
