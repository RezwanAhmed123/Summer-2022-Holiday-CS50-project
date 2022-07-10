# Generated by Django 4.0.5 on 2022-07-10 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bids_bidder_alter_bids_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='current_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bids',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_for_item', to='auctions.listings'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]