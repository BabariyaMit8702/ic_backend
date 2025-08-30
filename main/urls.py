from . import views
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('',views.the_second),
    path('access/',TokenObtainPairView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    
    ]

