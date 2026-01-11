from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property

# Create your views here.

@cache_page(60 * 15)  # Cache for 15 minutes (900 seconds)
def property_list(request):
    properties = Property.objects.all().values('id', 'title', 'description', 'price', 'location', 'created_at')
    return JsonResponse({"data": list(properties)}, safe=False)
