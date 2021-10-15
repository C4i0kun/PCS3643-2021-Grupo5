from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from .models import Lote, Leilao, Lance

# Forms
class LoteForm(ModelForm):
    class Meta:
        model = Lote
        fields = ['name', 'numero_sequencial', 'descricao', 'estado', 
                  'taxa_de_comissao', 'valor_minimo_de_lote',
                  'valor_minimo_de_reserva', 'valor_minimo_por_lance']

class LeilaoForm(ModelForm):
    class Meta:
        model = Leilao
        fields = ['name', 'periodoInicio', 'periodoFinal']  

class LanceForm(ModelForm):
    class Meta:
        model = Lance
        fields = ['valor']

# funções dos lotes
@login_required
def principal(request, template_name='catalogo/principal.html'):
    
    leiloes = Leilao.objects.all()
    lances = Lance.objects.all()

    data = {}
    data['lista_de_leiloes'] = leiloes

    # Pegar maior lance depois

    return render(request, template_name, data)

# funções dos lotes
@login_required
def lista_lote(request, template_name='catalogo/lista_lote.html'):
    if request.user.is_superuser:
        lotes = Lote.objects.all()
    else:
        lotes = Lote.objects.filter(vendedor=request.user)

    # leiloes = Leilao.objects.all()
    # lances = Lance.objects.all()

    data = {}
    data['lista_de_lotes'] = lotes
    # data['lista_de_leiloes'] = leiloes
    # data['lista_de_lances'] = lances

    data['lista_de_lotes_disponiveis'] = []
    for lote in lotes:
        if not Leilao.objects.filter(lote = lote):
            data['lista_de_lotes_disponiveis'].append(lote)

    return render(request, template_name, data)

@login_required
def detalha_lote(request, pk, template_name='catalogo/detalha_lote.html'):
    if request.user.is_superuser:
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, vendedor=request.user)

    data = {}
    data['lote'] = lote

    return render(request, template_name, data)

@login_required
def cria_lote(request, template_name='catalogo/lote_form.html'):
    form = LoteForm(request.POST or None)
    if form.is_valid():
        lote = form.save(commit=False)
        lote.vendedor = request.user
        lote.save()
        return redirect('catalogo:detalha_lote', pk=lote.id)
    return render(request, template_name, {'form':form})

@login_required
def atualiza_lote(request, pk, template_name='catalogo/lote_form.html'):
    if request.user.is_superuser:
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, vendedor=request.user)
    form = LoteForm(request.POST or None, instance=lote)
    if form.is_valid():
        form.save()
        return redirect('catalogo:detalha_lote', pk=pk)
    return render(request, template_name, {'form':form})

@login_required
def deleta_lote(request, pk, template_name='catalogo/lote_confirma_delecao.html'):
    if request.user.is_superuser:
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, vendedor=request.user)
    if request.method=='POST':
        lote.delete()
        return redirect('catalogo:lista_lote')
    return render(request, template_name, {'object':lote})

# funções dos leilões
@login_required
def lista_leilao(request, template_name='catalogo/lista_leilao.html'):
    leiloes = Leilao.objects.all()
    lances = Lance.objects.all()

    data = {}
    data['lista_de_leiloes'] = leiloes
    data['lista_de_lances'] = sorted(lances, key=lambda t: t.valor, reverse=True)

    return render(request, template_name, data)

@login_required
def cria_leilao(request, id_lote, template_name='catalogo/leilao_form.html'):
    form = LeilaoForm(request.POST or None)
    if form.is_valid():
        leilao = form.save(commit=False)
        lote = get_object_or_404(Lote, pk=id_lote)
        leilao.lote = lote
        leilao.save()
        return redirect('catalogo:detalha_leilao', pk=leilao.id)
    return render(request, template_name, {'form':form})

@login_required
def detalha_leilao(request, pk, template_name='catalogo/detalha_leilao.html'):
    leilao= get_object_or_404(Leilao, pk=pk)
    lances = Lance.objects.all()

    data = {}
    data['leilao'] = leilao
    data['lista_de_lances'] = sorted(lances, key=lambda t: t.valor, reverse=True)

    return render(request, template_name, data)

@login_required
def atualiza_leilao(request, pk, template_name='catalogo/leilao_form.html'):
    leilao= get_object_or_404(Leilao, pk=pk)
    
    form = LeilaoForm(request.POST or None, instance=leilao)
    if form.is_valid():
        form.save()
        return redirect('catalogo:detalha_leilao', pk=pk)
    return render(request, template_name, {'form':form})

@login_required
def deleta_leilao(request, pk, template_name='catalogo/leilao_confirma_delecao.html'):
    leilao= get_object_or_404(Leilao, pk=pk)
    
    if request.method=='POST':
        leilao.delete()
        return redirect('catalogo:lista_leilao')
    return render(request, template_name, {'object':leilao})

@login_required
def faz_lance(request, id_leilao, template_name='catalogo/lance_form.html'):
    form = LanceForm(request.POST or None)
    if form.is_valid():
        lance = form.save(commit=False)
        leilao = get_object_or_404(Leilao, pk=id_leilao)
        lance.leilao = leilao
        lance.comprador = request.user
        lance.save()
        return redirect('catalogo:detalha_leilao', pk=id_leilao)
    return render(request, template_name, {'form':form})