from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 
from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Importando o modelo de usuário personalizado

class CustomUserCreationForm(UserCreationForm):
    # Adicionando campos personalizados
    email = forms.EmailField(max_length=254,)

    class Meta:
        model = CustomUser  # Substituindo pelo modelo de usuário personalizado
        fields = UserCreationForm.Meta.fields + ('email',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # Remove os help_texts automáticos do Django
        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['password1'].help_text = mark_safe('<ul class="custom-help-text">'
                                                       '<li>Sua senha não pode ser muito parecida com o resto das suas informações pessoais.</li>'
                                                       '<li>Sua senha precisa conter pelo menos 8 caracteres.</li>'
                                                       '<li>Sua senha não pode ser uma senha comumente utilizada.</li>'
                                                       '<li>Sua senha não pode ser inteiramente numérica.</li>'
                                                       '</ul>')
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Um usuário com este endereço de e-mail já existe.', code='email_exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Um usuário com este nome de usuário já existe.', code='username_exists')
        return username

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'status')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise forms.ValidationError("O título é obrigatório.")
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError("Um post com este título já existe.")
        
        return title
    