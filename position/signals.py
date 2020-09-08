from django.core.cache        import cache
from django.core.signals      import request_finished
from django.db.models.signals import post_save, post_delete
from django.dispatch          import receiver, Signal

from .models import Position

@receiver(request_finished)
def position_view_callback(sender, **kwargs):
    print('request accpeted')

@receiver(post_save, sender = Position)
@receiver(post_delete, sender = Position)
def invalidate_position_cache(sender, instance, **kwargs):
    cache.delete('positions')
