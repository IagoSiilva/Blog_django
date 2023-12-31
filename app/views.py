from django.shortcuts import render, redirect
from .models import Post, Comment
from django.views import generic
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from app.models import CustomUser
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

def Base(request):
    return render(request, 'base.html')
# lista de Posts
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    context_object_name = 'posts' #Passando o contexto ao renderizar a página index.html na visão PostList
    paginate_by = 10  # Número de posts por página


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        
        try:
            posts = context['posts']
        except KeyError:
            posts = self.object_list
        
        paginator = context['paginator']
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts

        return context

def about(request):
    return render(request, 'about.html') #Página sobre


#Pesquisar Posts
def search_posts(request):
    query = request.GET.get('q')
    
    # Adicionando o filtro nos posts
    if query:
        post_list = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        post_list = Post.objects.all()

    title = f"Resultados de Pesquisa para: {query}" if query else "Pesquisa"
    # Configurando a paginação
    paginator = Paginator(post_list, 10)  # Mostrar 10 posts por página
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não é um número, entrega a primeira página.
        posts = paginator.page(1)
    except EmptyPage:
        # Se a página está fora dos limites (e.g. 9999), entrega a última página de resultados.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'search_results.html', {'posts': posts, 'query': query})
#Adicionar comentário
def add_comment(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        text = request.POST['text']
        author = request.user
        Comment.objects.create(post=post, author=author, text=text)

    return redirect('post_detail', slug=slug)


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

# def like_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)

#     # Incrementa o número de likes
#     post.likes += 1
#     post.save()

#     # Redireciona de volta à página de detalhes do post
#     return redirect('post_detail', slug=post.slug)

@login_required # Somente os usuários autenticados possam acessar a página de criação de post.
def create_post(request):
        hide_navbar = True
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)  # Usar commit=False para evitar salvar o objeto no banco de dados ainda
                post.author = request.user  # Define o autor da postagem como o usuário autenticado
                print(f"Author: {post.author}") #debugando retirar isso depois
                post = form.save()
                return redirect('home')  # Redireciona para a página do post criado
        else:
            form = PostForm()
        return render(request, 'create_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('user_profile', username=request.user.username)

    context = {'post': post}
    return render(request, 'delete_post.html', context)

def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    # Excluindo rascunhos da consulta dos posts do usuário
    user_posts = Post.objects.filter(author=user, status=Post.PUBLISHED).order_by('-created_on')

    context = {
        'username': username,
        'user_posts': user_posts,
    }

    return render(request, 'user_profile.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = PostForm(instance=post)

    context = {'form': form, 'post': post}
    return render(request, 'edit_post.html', context)


@login_required
def drafts_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    drafts = Post.objects.filter(author=user, status=0).order_by('-created_on')

    paginator = Paginator(drafts, 10)  # Mostrar 10 rascunhos por página
    page = request.GET.get('page')

    try:
        drafts = paginator.page(page)
    except PageNotAnInteger:
        drafts = paginator.page(1)
    except EmptyPage:
        drafts = paginator.page(paginator.num_pages)

    context = {
        'username': username,
        'drafts': drafts,
    }

    return render(request, 'drafts_list.html', context)
# def home(request):
#     return render(request, "app/home.html")

def publish_draft(request, username, draft_id):
    user = get_object_or_404(CustomUser, username=username)
    draft = get_object_or_404(Post, id=draft_id, author=user, status=Post.DRAFT)

    # Atualizar a data do rascunho para a data atual
    draft.publish_date = timezone.now()

    # Alterar o status do rascunho para publicado
    draft.status = Post.PUBLISHED
    
    # Salvar as alterações no rascunho
    draft.save()

    return redirect('drafts_list', username=username)