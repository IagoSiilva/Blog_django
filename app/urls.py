from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import delete_post
from .views import edit_post



urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create/', views.create_post, name='create_post'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('registro/', views.register, name='register'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('sobre/', views.about, name='about'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('post/<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('search/', views.search_posts, name='search_posts'),
    path('<slug:slug>/', views.DetailView.as_view(), name='post_detail'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)