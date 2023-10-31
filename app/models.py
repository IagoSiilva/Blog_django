from django.db import models
from django.db.models import ImageField
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    nome_completo = models.CharField(max_length=255)
    # Outros campos personalizados

    def __str__(self):
        return self.username
    

def image_filename(instance, filename):
    # O nome do arquivo será no formato 'post_images/(ID do Post) nome do arquivo'
    return f'post_images/{instance.pk}_{filename}'

Status = ((0,  'Rascunho'), (1, 'Publicado'))

class Post(models.Model):
    #Título
    title = models.CharField(max_length=200, unique=True)
    #Subtítulo
    slug = models.SlugField(max_length=200, blank=True)
    #Autor do post (se eu deletar um usuário todos os outros post do autor será deletado)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='app_posts', null=True)
    #Data de criação da postagem
    created_on = models.DateTimeField(auto_now_add=True)
    #Data de atualização da postagem
    update_on = models.DateTimeField(auto_now=True)
    #Conteúdo
    content = models.TextField()
    #Status se foi ou não publicado
    status = models.IntegerField(choices=Status, default=0)
    #Imagem
    image = models.ImageField(upload_to='post_images/', null=True, blank=True) # post_images/ é o diretório onde as imagens serão armazenadas
    def save(self, *args, **kwargs):
        if not self.slug:  # Verifica se o slug ainda não foi preenchido
            self.slug = slugify(self.title)
            unique_slug = self.slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)


#tetes
    # image = models.ImageField(upload_to='post_images/')
    # image = models.ImageField(upload_to='post_images', default='path/to/default/image.jpg')

    class Meta:
        #Organização das Postagens do mais recente para o mais antigo
        ordering =  ["-created_on"]
    
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         img = Image.open(self.image.path)
    #         max_size = (300, 300)
    #         img.thumbnail(max_size)
    #         img.save(self.image.path)



def __str__(self):
    return self.title

