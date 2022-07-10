# Generated by Django 4.0.5 on 2022-07-10 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listings_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_made', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bids',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listings'),
        ),
    ]