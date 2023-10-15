from .models import ListingBid
from django.db.models.signals import post_save
from django.dispatch import receiver

#@receiver(post_save, sender=ListingBid)
#def update_current_price(sender, instance, **kwargs):
#    instance.for_listing.current_price = instance.bid_amount
#    instance.for_listing.current_price.save()