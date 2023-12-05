from django.urls import path
from . import views

app_name = 'webapp'


urlpatterns = [
    path('',views.feed, name="feed"),
    path('addphoto/', views.addphoto, name="addphoto"),
    path('signup/', views.signup, name="signup"),
    path('profilecustomization/', views.profilecustomization, name="profilecustomization" ),
    path('profileupdate/', views.update_profile, name="profileuptade" ),
    path('userprofile/', views.userprofile, name="userprofile" ),
    path('deletephoto/<int:id>', views.deletephoto, name="deletephoto"),
    path('search/', views.search, name="search"),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('searchprofile/', views.search_profile, name="searchprofile" ),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('user_selected_profile/<int:id>', views.user_selected_profile, name='user_selected_profile')
]