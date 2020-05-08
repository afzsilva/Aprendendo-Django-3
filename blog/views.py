from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag

path_lista = 'blog/post/list.html'
path_detalhe = 'blog/post/detail.html'

# Create your views here.
# def post_list(request, tag_slug=None):
#     """Função que recebe request e retorna a lista de póstagens"""
#     posts = Post.published.all() # chamada do manager model customisado
#     tag = None
#
#     if tag_slug:
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         object_list = posts.filter(tags__in=[tag])
#     paginator = Paginator(object_list, 3)
#
#
#     return render(request,path_lista,{'posts':posts})




def post_list(request, tag_slug=None):
    """Faz a paginação"""
    object_list = Post.published.all() # queryset
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) #Três posts por pagina
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Entrega a primeira pagina se não for inteiro
        posts = paginator.page(1)
    except EmptyPage:
        # se não tiver dentro do intervalo entrega as ultimas paginas como resultado
        posts = paginator.page(paginator.num_pages)
    return render(request,path_lista,{'page':page,
                                      'posts': posts,
                                      'tag':tag,})





def post_detail(request, year, month, day, post):
    """mostra os detalhes de uma unica postagem"""
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # lista de comentarios para este post
    comments = post.comments.filter(active=True) # recupera todos comentários ativos

    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    #lista de posts similares
    post_tags_id = post.tags.values_list('id', flat=True)

    similar_posts = Post.published.filter(tags__in=post_tags_id)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]


    return render(request, path_detalhe, {'post':post,
                                          'comments':comments,
                                          'new_comment':new_comment,
                                          'comment_form':comment_form,
                                          'similar_posts':similar_posts})





class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = path_lista





def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #Enviar email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f" {cd['name']} recomendado que voce leia "\
                      f"{post.title}"
            message = f"Ler {post.title} em {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'afranio26@yahoo.com.br',[cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,
                                                  'form':form,
                                                  'sent':sent})
