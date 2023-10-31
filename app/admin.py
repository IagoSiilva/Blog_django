from django.contrib import admin
from .models import Post
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')  # Escolha quais campos você deseja exibir na lista de usuários
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Adicione os campos pelos quais você deseja buscar usuários

admin.site.register(CustomUser, CustomUserAdmin)

# class PostAdmin(admin.ModelAdmin):

admin.site.register(Post)

