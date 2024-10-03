from django.urls import path
from FrontEnd import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('save_register/', views.save_register, name='save_register'),
    path('save_login/', views.save_login, name='save_login'),
    path('logout/', views.logout, name='logout'),
    path('blog/', views.blog, name='blog'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profilecard/<int:user_id>/', views.profilecard, name='profilecard'),
    path('save_blog_user/', views.save_blog_user, name='save_blog_user'),
    path('blogform/', views.blogform, name='blogform'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('list/', views.blog_list, name='list'),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    ]
