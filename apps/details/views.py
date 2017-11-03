from rest_framework import viewsets,mixins,pagination,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

from .serializer import DetailSerializer
from .models import Detail
from .filters import DetailFilter


class Page(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class DetailListViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer
    pagination_class = Page
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    filter_class = DetailFilter
    search_fields = ('title', 'content')
    ordering_fields = ('title', 'add_time')