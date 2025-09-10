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
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    is_followed_by_me = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields = '__all__'

    def get_profile_pic_url(self, obj):
        request = self.context.get('request')
        if obj.profile_pic:
            return request.build_absolute_uri(obj.profile_pic.url)
        return None
    
    def get_followers_count(self, obj):
        return Follow.objects.filter(user=obj.user).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj.user).count()

    def get_followers(self, obj):
        followers = Follow.objects.filter(user=obj.user)
        return [
            {
                "username": f.follower.username,
                "profile_id": f.follower.profile.Profile_id,
                "profile_pic": (
                    self.context["request"].build_absolute_uri(f.follower.profile.profile_pic.url)
                    if f.follower.profile.profile_pic else None
                )
            }
            for f in followers
        ]

    def get_following(self, obj):
        followings = Follow.objects.filter(follower=obj.user)
        return [
            {
                "username": f.user.username,
                "profile_id": f.user.profile.Profile_id,
                "profile_pic": (
                    self.context["request"].build_absolute_uri(f.user.profile.profile_pic.url)
                    if f.user.profile.profile_pic else None
                )
            }
            for f in followings
        ]
    
    def get_is_followed_by_me(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(user=obj.user, follower=request.user).exists()
        return False


class PostSerializer(serializers.ModelSerializer):
    post_url = serializers.SerializerMethodField(read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked_by_user = serializers.SerializerMethodField(read_only=True)
    user_profile_pic = serializers.SerializerMethodField(read_only=True)
    user_profile_id = serializers.SerializerMethodField(read_only=True) 
    
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
    
    def get_user_profile_pic(self, obj):
        request = self.context.get('request')
        try:
            profile = Profile.objects.get(user=obj.user)
            if profile.profile_pic:
                return request.build_absolute_uri(profile.profile_pic.url)
        except Profile.DoesNotExist:
            return None
        return None
    
    
    def get_user_profile_id(self, obj):   
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.Profile_id  
        except Profile.DoesNotExist:
            return None
    
    
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)
    user_profile_pic = serializers.SerializerMethodField(read_only=True)
    user_profile_id = serializers.SerializerMethodField(read_only=True) 


    class Meta:
        model = Comment
        fields = '__all__'

    def get_user_profile_pic(self, obj):
        request = self.context.get('request')
        try:
            profile = Profile.objects.get(user=obj.user)
            if profile.profile_pic:
                return request.build_absolute_uri(profile.profile_pic.url)
        except Profile.DoesNotExist:
            return None
        return None
    
    
    def get_user_profile_id(self, obj):   
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.Profile_id  
        except Profile.DoesNotExist:
            return None


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'