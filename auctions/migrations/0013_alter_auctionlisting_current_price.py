# Generated by Django 4.2.6 on 2023-10-16 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_auctionlisting_current_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
