from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
  path('', views.lista_lote_leilao, name='lista_lote_leilao'),
  path('lote/new/', views.cria_lote, name='cria_lote'),
  path('lote/edit/<int:pk>/', views.atualiza_lote, name='atualiza_lote'),
  path('lote/delete/<int:pk>/', views.deleta_lote, name='deleta_lote'),
  path('leilao/new/<int:id_lote>/', views.cria_leilao, name='cria_leilao'),
  path('leilao/edit/<int:pk>/', views.atualiza_leilao, name='atualiza_leilao'),
  path('leilao/delete/<int:pk>/', views.deleta_leilao, name='deleta_leilao'),
  path('lance/new/<int:id_leilao>/', views.faz_lance, name='faz_lance'),
]