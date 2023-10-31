from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Importando o modelo de usuário personalizado

class CustomUserCreationForm(UserCreationForm):
    # Adicionando campos personalizados
    email = forms.EmailField(max_length=254, help_text='Obrigatório. Por favor insira um endereço de e-mail válido')

    class Meta:
        model = CustomUser  # Substituindo pelo modelo de usuário personalizado
        fields = UserCreationForm.Meta.fields + ('email',)  # Adicionando quaisquer campos adicionais aqui


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'status')

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise forms.ValidationError("O título é obrigatório.")
        return title