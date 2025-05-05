from django.contrib import admin
from django.urls import path
from vendas import views

urlpatterns = [
    path('', views.vendas, name='vendas'),
    path('admin/', admin.site.urls),
    path('produtos/', views.consulta, name='listar_produtos'),
    path('produtos/cadastrar/', views.cadastrar_item, name='cadastrar_item'),
    path('produtos/<int:produto_est>/editar/', views.editar_produto, name='editar_produto'),
]
