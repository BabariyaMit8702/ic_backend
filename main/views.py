from django.shortcuts import render,HttpResponse
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework import viewsets,status
from rest_framework.response import Response


# Create your views here.
def the_first(request):
    return HttpResponse('MY APP')

def the_second(request):
    return HttpResponse('MY API')

class UserApi(viewsets.ViewSet):

    def list(self,request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        new = request.data
        serializer = UserSerializer(data=new)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)