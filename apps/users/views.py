# from rest_framework import viewsets, mixins, pagination, filters
# from django_filters.rest_framework import DjangoFilterBackend

# from .serializer import UserProfileSerializer
# from .models import UserProfile
# from .filters import UserProfileFilter


# class Page(pagination.PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     page_query_param = 'p'
#     max_page_size = 100


# class UserProfileListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     pagination_class = Page
#     filter_backends = (DjangoFilterBackend,
#                        filters.SearchFilter, filters.OrderingFilter,)
#     filter_class = UserProfileFilter
#     search_fields = ('username', 'email')
#     ordering_fields = ('username', 'email')
from random import choice


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response


from .serializer import VerifyCodeSerializer, UserRegSerializer
from .models import VerifyCode


User = get_user_model()


class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    '''

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class VerifyCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = VerifyCodeSerializer
    queryset = VerifyCode.objects.all()

    def generate_code(self):
        codes = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(codes))

        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = self.generate_code()
        verifycode = VerifyCode(code=code, email=email)
        verifycode.save()
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
