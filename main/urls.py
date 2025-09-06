from . import views
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user-api',views.UserApi,basename='user')
router.register(r'my-profile',views.ProfileApi,basename='my_profile')
router.register(r'posts',views.PostApi,basename='post-deatails')
router.register(r'likes',views.LikeApi,basename='like-details')
router.register(r'comments',views.CommentApi,basename='comment-details')
router.register(r'like-management',views.ToggleLikeViewSet,basename='like-management')
router.register(r'follow',views.FollowApi,basename='follow-ops')

urlpatterns = [
    path('',views.the_second),
    path('access/',views.MyCustomTOP.as_view()),
    path('refresh/',views.MyCUSREF.as_view()),
    path('home-page-feed',views.Homepage.as_view(),name='home-feed'),
    path('api/',include(router.urls)),
    ]


