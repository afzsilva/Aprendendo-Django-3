from django.urls import path
from . import views
""" url do APP
Arquivo onde é definido as url que serão incluidas no arquivo url.py do projeto
"""

app_name = 'blog'

urlpatterns = [
    # post views

    # chamada do template da view listagem atraves de uma função
    path('',views.post_list, name='post_list'),

    #URL Pattern para lista de tags
    path('tag/<slug:tag_slug>',views.post_list, name='post_list_by_tag'),


    # Chamada da view Listagem usando o conceito de class-based views
    #path('',views.PostListView.as_view(), name='post_list'),


    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share')
]