# Generated by Django 3.2 on 2021-05-04 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_highestbid_listing_startingbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('Collectibles & Art', 'Collectibles & Art'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Home & Garden', 'Home & Garden'), ('Motors', 'Motors'), ('Sport', 'Sport'), ('Toys & hobbies', 'Toys & hobbies'), ('Other Catagories', 'Other Catagories')], max_length=64),
        ),
    ]
