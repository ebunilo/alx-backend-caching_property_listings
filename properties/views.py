from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties

# Create your views here.

@cache_page(60 * 15)  # Cache for 15 minutes (900 seconds)
def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties}, safe=False)
