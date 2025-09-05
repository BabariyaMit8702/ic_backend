from django.shortcuts import HttpResponse,get_object_or_404
from .serializers import UserSerializer,MyCustomTOPSerializer,ProfileSerializer,PostSerializer,LikeSerializer,CommentSerializer
from .models import CustomUser,Profile,Post,Like,Comment
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import action



User = get_user_model()


# Create your views here.
def the_first(request):
    return HttpResponse('MY BACKEND')

def the_second(request):
    return HttpResponse('MY API')

class UserApi(viewsets.ViewSet):

    def get_permissions(self):
        if(self.action == 'list'):
            return [IsAuthenticated()]
        return []

    def list(self,request):
        users = CustomUser.objects.filter(username=request.user.username)
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        new = request.data
        serializer = UserSerializer(data=new)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class MyCustomTOP(TokenObtainPairView):
    serializer_class = MyCustomTOPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data

        response = Response({'messege':'login succussfully!'},status=status.HTTP_200_OK)

        access_token = tokens['access']
        refresh_token = tokens['refresh']

        access_exp = timezone.now() + timedelta(minutes=100)
        refresh_exp = timezone.now() + timedelta(days=31)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='None',
            path='/',
            expires=access_exp
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='None',
            path='/',
            expires=refresh_exp
        )

        return response
    
class MyCUSREF(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token =request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'error':'not found from cookies'},status=status.HTTP_400_BAD_REQUEST)
        
        serilizer = self.get_serializer(data={'refresh':refresh_token})
        serilizer.is_valid(raise_exception=True)
        access_token = serilizer.validated_data['access']

        response = Response({'messee':'refreshed succusflly'})

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='None',
            path='/',
            expires=timezone.now() + timedelta(minutes=100)
        )

        return response
    
class ProfileApi(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self,request,pk=None):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostApi(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class LikeApi(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  

    @action(detail=True, methods=['get'])
    def list_likes(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class ToggleLikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            return Response({"message": "Unliked"})
        return Response({"message": "Liked"})


class CommentApi(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]