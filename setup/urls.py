
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
#Importando a views da aplicação na urls
# from app import views

#Rotas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('', home),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)