# Generated by Django 4.0.5 on 2022-07-09 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listings_current_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='current_bidder',
        ),
    ]
