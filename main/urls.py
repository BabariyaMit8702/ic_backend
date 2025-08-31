from . import views
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user-api',views.UserApi,basename='user')

urlpatterns = [
    path('',views.the_second),
    path('access/',TokenObtainPairView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('api/',include(router.urls)),
    ]

