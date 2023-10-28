
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
#Importando a views da aplicação na urls
# from app import views

#Rotas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('app.urls')),


    # path('', home),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)