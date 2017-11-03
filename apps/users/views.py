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


from rest_framework import viewsets, status,mixins,permissions,authentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


from .serializer import VerifyCodeSerializer, UserRegSerializer,UserDetailSerializer
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


class VerifyCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
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
        return Response(code, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

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
    
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
