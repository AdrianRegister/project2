# Generated by Django 4.2.6 on 2023-10-14 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='listing_description',
            field=models.TextField(default='Default description', max_length=5120),
        ),
    ]