from datetime import datetime, timedelta

from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


from .models import VerifyCode


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

    def validate_email(self, email):
        '''
        验证邮箱
        '''
        # 邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError('该邮箱已被注册')
        # 查看验证码是否重复发送过
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, email=email).count():
            raise serializers.ValidationError('请稍后60秒')
        return email


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, required=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(
            email=self.initial_data['email']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago < last_record.add_time:
                raise serializers.ValidationError('验证码已过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

        return code

    def validate(self, attrs):
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ['username', 'email', 'code', 'password']
