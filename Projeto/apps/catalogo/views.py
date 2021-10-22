from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

from datetime import datetime, timezone, timedelta

from .models import Lote, Leilao, Lance

# Forms
class LoteForm(ModelForm):
    class Meta:
        model = Lote
        fields = ['name', 'descricao', 'estado', 
                  'valor_minimo_de_lote', 'valor_minimo_de_reserva', 'valor_minimo_por_lance']

    def clean_valor_minimo_de_lote(self):
        valor_minimo_de_lote = self.cleaned_data['valor_minimo_de_lote']

        # Checa se o valor mínimo do lote é superior a zero.
        if float(valor_minimo_de_lote) <= 0:
            raise ValidationError(_('Valor mínimo do lote deve ser superior a 0.'))

        return valor_minimo_de_lote
     
    def clean_valor_minimo_de_reserva(self):
        valor_minimo_de_lote = self.data['valor_minimo_de_lote']
        valor_minimo_de_reserva = self.cleaned_data['valor_minimo_de_reserva']

        # Checa se o valor mínimo de reserva é superior a zero.
        if float(valor_minimo_de_reserva) <= 0:
            raise ValidationError(_('Valor mínimo de reserva deve ser superior a 0.'))

        # Checa se o valor mínimo de reserva é superior ao valor mínimo de lote.
        if float(valor_minimo_de_reserva) <= float(valor_minimo_de_lote):
            raise ValidationError(_('Valor mínimo de reserva deve ser superior ao valor mínimo do lote.'))

        return valor_minimo_de_reserva
    
    def clean_valor_minimo_por_lance(self):
        valor_minimo_por_lance = self.cleaned_data['valor_minimo_por_lance']

        # Checa se o valor mínimo por lance é superior a zero.
        if float(valor_minimo_por_lance) <= 0:
            raise ValidationError(_('Valor mínimo por lance deve ser superior a 0.'))

        return valor_minimo_por_lance

class LeilaoForm(ModelForm):
    class Meta:
        model = Leilao
        fields = ['name', 'periodoInicio', 'periodoFinal']  

    # def clean_periodoInicio(self):
    #     periodoInicio = self.cleaned_data['periodoInicio']
    #     periodoFinal = self.data['periodoFinal']

    #     # Checa se o início do período é posterior ao horário atual.
    #     if periodoInicio.replace(tzinfo=utc) < datetime.now(timezone.utc):
    #         raise ValidationError(_('Início do período do leilão deve ser posterior ao horário atual.'))

    #     # Checa se o início do período é anterior ao final do período.
    #     if periodoInicio.replace(tzinfo=utc) >= periodoFinal.replace(tzinfo=utc):
    #         raise ValidationError(_('Início do período do leilão deve ser anterior ao final do período do leilão.'))

    #     return periodoInicio

    # def clean_periodoFinal(self):
    #     periodoInicio = self.data['periodoInicio']
    #     periodoFinal = self.cleaned_data['periodoFinal']

    #     # Checa se o início do período é posterior ao horário atual.
    #     if periodoFinal.replace(tzinfo=utc) < datetime.now(timezone.utc) + timedelta(days=1):
    #         raise ValidationError(_('Final do período do leilão deve ser posterior ao horário atual mais um dia.'))

    #     # Checa se o início do período é anterior ao final do período.
    #     if periodoFinal.replace(tzinfo=utc) < periodoInicio.replace(tzinfo=utc) + timedelta(days=1):
    #         raise ValidationError(_('Final do período do leilão deve ser posterior ao início do período do leilão mais um dia.'))

    #     return periodoFinal

class LanceForm(ModelForm):
    class Meta:
        model = Lance
        fields = ['valor']

    def clean_valor(self):
        valor = self.cleaned_data['valor']

        # Checa se o valor é superior a zero.
        if float(valor) <= 0:
            raise ValidationError(_('Valor deve ser superior a 0.'))

        return valor

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

        if lote.valor_minimo_de_lote <= 1000:
            lote.taxa_de_comissao = 1/100
        elif lote.valor_minimo_de_lote <= 10000:
            lote.taxa_de_comissao = 2/100
        elif lote.valor_minimo_de_lote <= 50000:
            lote.taxa_de_comissao = 3/100
        elif lote.valor_minimo_de_lote <= 100000:
            lote.taxa_de_comissao = 4/100
        else:
            lote.taxa_de_comissao = 5/100

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