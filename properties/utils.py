from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Get all properties from cache or database.
    Checks Redis for 'all_properties' using cache.get('all_properties').
    Fetches Property.objects.all() if not found.
    Stores the queryset in Redis with cache.set('all_properties', queryset, 3600).
    Returns the queryset.
    """
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values('id', 'title', 'description', 'price', 'location', 'created_at'))
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour (3600 seconds)
    return properties