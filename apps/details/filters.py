import django_filters
from .models import Detail

class DetailFilter(django_filters.rest_framework.FilterSet):
    
    class Meta:
        model = Detail
        fields = ['add_time','title']