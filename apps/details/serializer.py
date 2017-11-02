from rest_framework import  serializers

from .models  import Detail
# from users.models import UserProfile

# class UserSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = UserProfile
#             fields = ['username']
            
            
class DetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Detail
        fields = '__all__'