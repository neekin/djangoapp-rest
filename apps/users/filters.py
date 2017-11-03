import django_filters
from .models import UserProfile


class UserProfileFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = UserProfile
        fields = ['username', ]
