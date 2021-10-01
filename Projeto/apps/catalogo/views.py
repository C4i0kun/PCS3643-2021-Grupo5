from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Lote

class LoteForm(ModelForm):
    class Meta:
        model = Lote
        fields = ['name', 'numero_sequencial', 'descricao', 'estado', 
                  'taxa_de_comissao', 'valor_minimo_de_lote',
                  'valor_minimo_de_reserva', 'valor_minimo_por_lance']

@login_required
def lista_lote(request, template_name='catalogo/lista_lote.html'):
    if request.user.is_superuser:
        lote = Lote.objects.all()
    else:
        lote = Lote.objects.filter(user=request.user)
    data = {}
    data['object_list'] = lote
    return render(request, template_name, data)

@login_required
def cria_lote(request, template_name='catalogo/lote_form.html'):
    form = LoteForm(request.POST or None)
    if form.is_valid():
        lote = form.save(commit=False)
        lote.user = request.user
        lote.save()
        return redirect('catalogo:lista_lote')
    return render(request, template_name, {'form':form})

@login_required
def atualiza_lote(request, pk, template_name='catalogo/lote_form.html'):
    if request.user.is_superuser:
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, user=request.user)
    form = LoteForm(request.POST or None, instance=lote)
    if form.is_valid():
        form.save()
        return redirect('catalogo:lista_lote')
    return render(request, template_name, {'form':form})

@login_required
def deleta_lote(request, pk, template_name='catalogo/lote_confirma_delecao.html'):
    if request.user.is_superuser:
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, user=request.user)
    if request.method=='POST':
        lote.delete()
        return redirect('catalogo:lista_lote')
    return render(request, template_name, {'object':lote})
