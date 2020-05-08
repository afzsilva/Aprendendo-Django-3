"""
Fonte de aprendisado : Livro Django 3 by Example
Paginas : 10, 11
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.


class PublishedManager(models.Manager):
    """ Essa classe é um gerenciador de models customisado
    ela retorna uma lista de postagem com status published
    manage custom ver pag-25
    """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')





class Post(models.Model):
    """ Esta classe define o modelo de dados para a entidade Post
        Nome tabela
        Atrinutos da tabela + tipo de dados
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateField(default=timezone.now())
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='draft')

    """Model managers"""
    objects = models.Manager() # manager default
    published = PublishedManager() # manager custom
    tags = TaggableManager() #Gerenciador de Tags

    def get_absolute_url(self):
        """Canonical URL"""
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


    class Meta:
        """
        Esta classe diz para django
        # 1 ordena os resultados das querys pelo campo publish na forma desc desc
        # 2 O campo title será visivél em locais como Admin e outros ...
        """
        ordering = ('-publish',) # 1
    def __str__(self): # 2
        return self.title




class Comment(models.Model):
    """ Modelo de dados para a tabela comentários"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now =True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

        def __str__(self):
            return f'comment by {self.name} on {self.post}'








