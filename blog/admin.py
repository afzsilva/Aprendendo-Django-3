from django.contrib import admin
from .models import Post, Comment

# Register your models here.
# admin.site.register(Post) substituido

@admin.register(Post) # registrando o model Post para o modulo de admin do django

class PostAdmin(admin.ModelAdmin):
    """ Essa classe customiza a forma como os models são exibidos no painel admin"""
    list_display = ('title','slug','author','publish','status') # capos da tabela
    list_filter = ('status','created','publish','author') # filtros na sidebar
    search_fields = ('title','body') # barra de pesquisa
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' # navegação por data
    ordering = ('status','publish') # forma de ordena a lista de post

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')