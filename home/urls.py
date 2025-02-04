from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria/', views.categoria, name="categoria"),
    path('categoria/form_categoria/', views.form_categoria, name="form_categoria"),
    path('categoria/detalhes/<int:id>/', views.detalhes_categoria, name="detalhes_categoria"),
    path('editar_categoria/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categoria/excluir/<int:id>/', views.excluir_categoria, name='excluir_categoria'),

######################################### CLIENTE ###############################################
    path('cliente/', views.cliente, name="cliente"),
    path('cliente/form_cliente/', views.form_cliente, name="form_cliente"),
    path('cliente/detalhes/<int:id>/', views.detalhes_cliente, name="detalhes_cliente"),
    path('editar_cliente/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),

######################################### PRODUTO ###############################################
    path('produto/', views.produto, name="produto"),
    path('produto/form_produto/', views.form_produto, name="form_produto"),
    path('produto/detalhes/<int:id>/', views.detalhes_produto, name="detalhes_produto"),
    path('produto/estoque/<int:id>/', views.ajustar_estoque, name="ajustar_estoque"),
    path('editar_produto/<int:id>/', views.editar_produto, name="editar_produto"),
    path('produto/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),

######################################## TESTES ##################################################
    path('teste1/', views.teste1, name='teste1'),
    path('teste2/', views.teste2, name='teste2'),
     path('teste3/', views.teste3, name='teste3'),
    path('buscar_dados/<str:app_modelo>/', views.buscar_dados, name='buscar_dados'),

###################################### PEDIDO #####################################################
    path('pedido/', views.pedido, name='pedido'),
    path('pedido/form/<int:id>/', views.novo_pedido, name='novo_pedido')

]

