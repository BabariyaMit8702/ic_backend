from . import views
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user-api',views.UserApi,basename='user')

urlpatterns = [
    path('',views.the_second),
    path('access/',views.MyCustomTOP.as_view()),
    path('refresh/',views.MyCUSREF.as_view()),
    path('api/',include(router.urls)),
    ]

