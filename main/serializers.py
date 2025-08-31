from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model,authenticate
from .models import CustomUser

mod_user = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class MyCustomTOPSerializer(TokenObtainPairSerializer):

    username_field = mod_user.USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
    def validate(self, attrs):

        credentials = {
            self.username_field:attrs.get('username'),
            'password':attrs.get('password')
        }

        the_user = authenticate(**credentials)
        if the_user is None:
            raise serializers.ValidationError('No Active Account Found')
        
        return super().validate(attrs)