from django.core.cache import cache
from django_redis import get_redis_connection
import logging

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


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Connects to Redis via django_redis, gets keyspace_hits and keyspace_misses from INFO,
    calculates hit ratio, logs metrics, and returns a dictionary.
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Get Redis connection
        redis_conn = get_redis_connection('default')
        
        # Get INFO stats
        info = redis_conn.info()
        
        # Extract keyspace hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) * 100 if total_requests > 0 else 0
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2)
        }
        
        # Log metrics
        logger.info(f"Redis Cache Metrics: Hits={keyspace_hits}, Misses={keyspace_misses}, "
                   f"Total={total_requests}, Hit Ratio={hit_ratio:.2f}%")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0
        }
