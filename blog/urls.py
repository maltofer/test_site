from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', PostView.as_view(), name='post'),
    path('article/<int:pk>', ArticleDetail.as_view(), name='article-detail'),
    path('addpost/', AddPostView.as_view(), name='add-post'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('like/<int:pk>', views.Like_post, name='like_post'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='profile'),
    path('<int:pk>/update_profile/', EditPofilePage.as_view(), name='update_profile'),
    path('article/<int:pk>/Comment/', AddCommentView.as_view(), name='comment'),
    path('contact/', views.contact_us, name='contact_us'),
] 