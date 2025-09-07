from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model,authenticate
from .models import CustomUser,Profile,Post,Like,Comment,Follow

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
    
class ProfileSerializer(serializers.ModelSerializer):
    profile_int_id = serializers.IntegerField(source='Profile_id', read_only=True)
    profile_pic_url = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def get_profile_pic_url(self, obj):
        request = self.context.get('request')
        if obj.profile_pic:
            return request.build_absolute_uri(obj.profile_pic.url)
        return None

class PostSerializer(serializers.ModelSerializer):
    post_url = serializers.SerializerMethodField(read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked_by_user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user', 'created_at'] 

    def get_post_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_like_count(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(post=obj, user=request.user).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['user','body']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'