from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post

path_lista = 'blog/post/list.html'
path_detalhe = 'blog/post/detail.html'

# Create your views here.
def post_list(request):
    """Função que recebe request e retorna a lista de póstagens"""
    posts = Post.published.all()
    return render(request,path_lista,{'posts':posts})

def post_detail(request, year, month, day, post):
    """mostra os detalhes de uma unia postagem"""
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, path_detalhe, {'post':post})

# def post_list(request):
#     """Faz a paginaçã"""
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3) #Três posts por pagina
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # Entrega a primeira pagina se não for inteiro
#         posts = paginator.page(1)
#     except EmptyPage:
#         # se não tiver dentro do intervalo entrega as ultimas paginas como resultado
#         posts = paginator.page(paginator.num_pages)
#     return render(request,path_lista,{'page':page,'posts': posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = path_lista