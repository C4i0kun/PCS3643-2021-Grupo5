from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
  path('', views.lista_lote, name='lista_lote'),
  path('new/', views.cria_lote, name='cria_lote'),
  path('edit/<int:pk>/', views.atualiza_lote, name='atualiza_lote'),
  path('delete/<int:pk>/', views.deleta_lote, name='deleta_lote'),
]