from django.shortcuts import render, redirect
from .models import Post
from django.views import generic
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from app.models import CustomUser

def Base(request):
    return render(request, 'base.html')

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    context_object_name = 'posts' #Passando o contexto ao renderizar a página index.html na visão PostList

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Quantidade de posts:", len(context['posts'])) # ===> Debugando Lembrar de Deletar depois <===
        return context

def about(request):
    return render(request, 'about.html') #Página sobre

class DetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

def user_login(request):
    hide_navbar = True # Escondendo navbar
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirecionar para a página inicial após o login
        else:
            # Tratar quando o login falhar
            # Poder renderizar uma mensagem de erro
            pass
    return render(request, 'registration/login.html', {'hide_navbar': hide_navbar})

def register(request):
    hide_navbar = True # Escondendo navbar
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autenticar o usuário após o registro
            return redirect('home')  # Redirecionar para a página inicial após o registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'hide_navbar': hide_navbar})


@login_required # Somente os usuários autenticados possam acessar a página de criação de post.
def create_post(request):
    hide_navbar = True
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Use commit=False para evitar salvar o objeto no banco de dados ainda
            post.author = request.user  # Define o autor da postagem como o usuário autenticado
            print(f"Author: {post.author}") #debugando retirar isso depois
            post = form.save()
            return redirect('home')  # Redireciona para a página do post criado
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def user_profile(request, username):
    # lógica para exibir o perfil do usuário com base no 'username'
    user = get_object_or_404(CustomUser, username=username)  # Obtém o usuário com base no nome de usuário do URL
    user_posts = Post.objects.filter(author=user)
    
    context = {
        'username': username,
        'user_posts': user_posts,
    }
    
    return render(request, 'user_profile.html', context)
# def home(request):
#     return render(request, "app/home.html")
