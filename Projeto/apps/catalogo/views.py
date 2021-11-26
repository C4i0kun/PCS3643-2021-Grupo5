from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.http import HttpResponse

from datetime import datetime, timezone, timedelta

from .models import CustomUser, Lote, Leilao, Lance
from .permissions import comprador_required, vendedor_required, leiloeiro_required, vendedor_or_leiloeiro_required, get_tipo_usuario
from .html_to_pdf import render_to_pdf

# Forms
class LoteForm(ModelForm):
    class Meta:
        model = Lote
        fields = ['name', 'descricao', 'estado', 'valor_minimo_de_reserva']

    # def clean_valor_minimo_de_lote(self):
    #     valor_minimo_de_lote = self.cleaned_data['valor_minimo_de_lote']

    #     # Checa se o valor mínimo do lote é superior a zero.
    #     if float(valor_minimo_de_lote) <= 0:
    #         raise ValidationError(_('Valor mínimo do lote deve ser superior a 0.'))

    #     return valor_minimo_de_lote
     
    def clean_valor_minimo_de_reserva(self):
        # valor_minimo_de_lote = self.data['valor_minimo_de_lote']
        valor_minimo_de_reserva = self.cleaned_data['valor_minimo_de_reserva']

        # Checa se o valor mínimo de reserva é superior a zero.
        if float(valor_minimo_de_reserva) <= 0:
            raise ValidationError(_('Valor mínimo de reserva deve ser superior a 0.'))

        # # Checa se o valor mínimo de reserva é superior ao valor mínimo de lote.
        # if float(valor_minimo_de_reserva) <= float(valor_minimo_de_lote):
        #     raise ValidationError(_('Valor mínimo de reserva deve ser superior ao valor mínimo do lote.'))

        return valor_minimo_de_reserva
    
    # def clean_valor_minimo_por_lance(self):
    #     valor_minimo_por_lance = self.cleaned_data['valor_minimo_por_lance']

    #     # Checa se o valor mínimo por lance é superior a zero.
    #     if float(valor_minimo_por_lance) <= 0:
    #         raise ValidationError(_('Valor mínimo por lance deve ser superior a 0.'))

    #     return valor_minimo_por_lance

class LeilaoForm(ModelForm):
    class Meta:
        model = Leilao
        fields = ['name', 'periodoInicio', 'periodoFinal']  

    def clean_periodoInicio(self):
        periodoInicio = self.cleaned_data['periodoInicio']
        periodoFinal = self.data['periodoFinal']

        if type(periodoInicio) == str:
            periodoInicio_dt = datetime.strptime(periodoInicio, '%Y-%m-%d %H:%M:%S')
        else:
            periodoInicio_dt = periodoInicio
        
        if type(periodoFinal) == str:
            periodoFinal_dt = datetime.strptime(periodoFinal, '%Y-%m-%d %H:%M:%S')
        else:
            periodoFinal_dt = periodoFinal

        # Checa se o início do período é posterior ao horário atual.
        if periodoInicio_dt.replace(tzinfo=utc) < datetime.now(timezone.utc):
            raise ValidationError(_('Início do período do leilão deve ser posterior ao horário atual.'))

        # Checa se o início do período é anterior ao final do período.
        if periodoInicio_dt.replace(tzinfo=utc) >= periodoFinal_dt.replace(tzinfo=utc):
            raise ValidationError(_('Início do período do leilão deve ser anterior ao final do período do leilão.'))

        return periodoInicio

    def clean_periodoFinal(self):
        periodoInicio = self.data['periodoInicio']
        periodoFinal = self.cleaned_data['periodoFinal']

        if type(periodoInicio) == str:
            periodoInicio_dt = datetime.strptime(periodoInicio, '%Y-%m-%d %H:%M:%S')
        else:
            periodoInicio_dt = periodoInicio
        
        if type(periodoFinal) == str:
            periodoFinal_dt = datetime.strptime(periodoFinal, '%Y-%m-%d %H:%M:%S')
        else:
            periodoFinal_dt = periodoFinal

        # Checa se o início do período é posterior ao horário atual.
        if periodoFinal_dt.replace(tzinfo=utc) < datetime.now(timezone.utc) + timedelta(days=1):
            raise ValidationError(_('Final do período do leilão deve ser posterior ao horário atual mais um dia.'))

        # Checa se o início do período é anterior ao final do período.
        if periodoFinal_dt.replace(tzinfo=utc) < periodoInicio_dt.replace(tzinfo=utc) + timedelta(days=1):
            raise ValidationError(_('Final do período do leilão deve ser posterior ao início do período do leilão mais um dia.'))

        return periodoFinal

class LanceForm(ModelForm):
    class Meta:
        model = Lance
        fields = ['valor']

    def __init__(self, *args,**kwargs):
        self.leilao = kwargs.pop('leilao')
        super(LanceForm, self).__init__(*args, **kwargs)

    def clean_valor(self):
        valor = self.cleaned_data['valor']

        # Checa se o valor é superior a zero.
        if float(valor) <= 0:
            raise ValidationError(_('Valor deve ser superior a 0.'))

        v_min_lote = self.leilao.lote.valor_minimo_de_lote

        # Checa se o valor é superior ao valor minimo de lote.
        if float(valor) < v_min_lote:
            raise ValidationError(_(f'Valor deve ser igual ou superior ao valor mínimo de lote: \
                                    R${v_min_lote}.'))

        lances = sorted(list(Lance.objects.filter(leilao__id=self.leilao.id)), key=lambda t: t.valor, reverse=True)
        if lances:
            valor_maior_lance = lances[0].valor
        else:
            valor_maior_lance = -10000

        v_por_lance = self.leilao.lote.valor_minimo_por_lance

        # Checa se o valor é superior ao valor minimo de lote.
        if float(valor) < valor_maior_lance + v_por_lance:
            raise ValidationError(_(f'Valor deve ser superior ao maior lance atual mais o valor mínimo por lance: \
                                    R${valor_maior_lance + v_por_lance}.'))

        return valor

# funções dos lotes
@login_required
def principal(request, template_name='catalogo/principal.html'):
    
    lances = Lance.objects.all()

    data = {}
    data['lista_de_leiloes_ativos'] = Leilao.objects.filter(status='A')
    data['tipo_usuario'] = get_tipo_usuario(request.user)

    # Pegar maior lance depois

    return render(request, template_name, data)

# funções dos lotes
@login_required
def lista_lote(request, template_name='catalogo/lista_lote.html'):
    if request.user.is_superuser or get_tipo_usuario(request.user) == 'L':
        lotes = Lote.objects.all()
    else:
        lotes = Lote.objects.filter(vendedor=request.user)

    data = {}
    data['lista_de_lotes'] = lotes
    data['lista_de_lotes_disponiveis'] = []
    for lote in lotes:
        if not Leilao.objects.filter(lote = lote).exclude(status='C'):
            data['lista_de_lotes_disponiveis'].append(lote)
            
    data['tipo_usuario'] = get_tipo_usuario(request.user)

    return render(request, template_name, data)

@login_required
def detalha_lote(request, pk, template_name='catalogo/detalha_lote.html'):
    if request.user.is_superuser or get_tipo_usuario(request.user) == 'L':
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, vendedor=request.user)

    data = {}
    data['lote'] = lote
    data['tipo_usuario'] = get_tipo_usuario(request.user)
    data['estado'] = lote.ESTADO_DICT[lote.estado]

    return render(request, template_name, data)

@login_required
@vendedor_required
def cria_lote(request, template_name='catalogo/lote_form.html'):
    form = LoteForm(request.POST or None)
    if form.is_valid():
        lote = form.save(commit=False)
        lote.vendedor = request.user

        lote.valor_minimo_de_lote = 0
        lote.valor_minimo_por_lance = 0
        lote.pago = False

        if lote.valor_minimo_de_reserva <= 1000:
            lote.taxa_de_comissao = 1/100
        elif lote.valor_minimo_de_reserva <= 10000:
            lote.taxa_de_comissao = 2/100
        elif lote.valor_minimo_de_reserva <= 50000:
            lote.taxa_de_comissao = 3/100
        elif lote.valor_minimo_de_reserva <= 100000:
            lote.taxa_de_comissao = 4/100
        else:
            lote.taxa_de_comissao = 5/100

        lote.save()
        return redirect('catalogo:detalha_lote', pk=lote.id)
    return render(request, template_name, {'form':form})

@login_required
@vendedor_required
def paga_lote(request, pk, template_name='catalogo/pagamento.html'):
    if request.user.is_superuser or get_tipo_usuario(request.user) == 'L':
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, vendedor=request.user)

    valor = lote.valor_minimo_de_reserva * lote.taxa_de_comissao

    data = {}
    data['valor'] = valor
    data['lote'] = lote

    if request.method == "POST":
        lote.pago = True

        lote.save()
        return redirect('catalogo:detalha_lote', pk=pk)

    return render(request, template_name, data)

@login_required
@vendedor_required
def atualiza_lote(request, pk, template_name='catalogo/lote_form.html'):
    if request.user.is_superuser or get_tipo_usuario(request.user) == 'L':
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, vendedor=request.user)
    
    form = LoteForm(request.POST or None, instance=lote)
    
    if form.is_valid():
        form.save()
        return redirect('catalogo:detalha_lote', pk=pk)
        
    return render(request, template_name, {'form':form})


@login_required
@leiloeiro_required
def insere_valores(request, pk, template_name='catalogo/insere_valores.html'):
    if request.user.is_superuser or get_tipo_usuario(request.user) == 'L':
        lote= get_object_or_404(Lote, pk=pk)
    else:
        lote= get_object_or_404(Lote, pk=pk, vendedor=request.user)
        
    if request.method == "POST":
        lote.valor_minimo_de_lote = request.POST.get("valor_minimo_de_lote", None)
        lote.valor_minimo_por_lance = request.POST.get("valor_minimo_por_lance", None)

        lote.save()
        return redirect('catalogo:detalha_lote', pk=pk)

    return render(request, template_name)

@login_required
@vendedor_or_leiloeiro_required
def deleta_lote(request, pk, template_name='catalogo/lote_confirma_delecao.html'):
    if request.user.is_superuser or get_tipo_usuario(request.user) == 'L':
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
    leiloes_nao_iniciados = Leilao.objects.filter(status='N')
    leiloes_ativos = Leilao.objects.filter(status='A')
    leiloes_finalizados = Leilao.objects.filter(status='F')
    leiloes_cancelados = Leilao.objects.filter(status='C')
    lances = Lance.objects.all()

    data = {}
    data['lista_de_leiloes_ativos'] = leiloes_ativos
    data['lista_de_leiloes_nao_iniciados'] = leiloes_nao_iniciados
    data['lista_de_leiloes_finalizados'] = leiloes_finalizados
    data['lista_de_leiloes_cancelados'] = leiloes_cancelados
    data['lista_de_lances'] = sorted(lances, key=lambda t: t.valor, reverse=True)

    return render(request, template_name, data)


@login_required
@leiloeiro_required
def cria_leilao(request, id_lote, template_name='catalogo/leilao_form.html'):
    form = LeilaoForm(request.POST or None)
    if form.is_valid():
        leilao = form.save(commit=False)
        lote = get_object_or_404(Lote, pk=id_lote)
        leilao.lote = lote
        leilao.status = "N"
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
    data['tipo_usuario'] = get_tipo_usuario(request.user) 
    data['status'] = leilao.STATUS_DICT[leilao.status]
    data['estado'] = leilao.lote.ESTADO_DICT[leilao.lote.estado]

    return render(request, template_name, data)

@login_required
@leiloeiro_required
def atualiza_leilao(request, pk, template_name='catalogo/leilao_form.html'):
    leilao= get_object_or_404(Leilao, pk=pk)
    
    form = LeilaoForm(request.POST or None, instance=leilao)
    if form.is_valid():
        form.save()
        return redirect('catalogo:detalha_leilao', pk=pk)
    return render(request, template_name, {'form':form})
    
@login_required
@leiloeiro_required
def inicia_leilao(request, pk, template_name='catalogo/detalha_leilao.html'):
    leilao= get_object_or_404(Leilao, pk=pk)
    
    leilao.status = 'A'
    leilao.save()

    return redirect('catalogo:detalha_leilao', pk=pk)
    
@login_required
@leiloeiro_required
def encerra_leilao(request, pk, template_name='catalogo/detalha_leilao.html'):
    leilao = get_object_or_404(Leilao, pk=pk)
    
    if len(list(Lance.objects.filter(leilao_id = leilao.id))) > 0:
        leilao.status = 'F'
    else:
        leilao.status = 'C'

    leilao.save()

    return redirect('catalogo:detalha_leilao', pk=pk)

@login_required
@leiloeiro_required
def cancela_leilao(request, pk, template_name='catalogo/detalha_leilao.html'):
    leilao= get_object_or_404(Leilao, pk=pk)
    
    leilao.status = 'C'
    leilao.save()

    return redirect('catalogo:detalha_leilao', pk=pk)

@login_required
@leiloeiro_required
def deleta_leilao(request, pk, template_name='catalogo/leilao_confirma_delecao.html'):
    leilao= get_object_or_404(Leilao, pk=pk)
    
    if request.method=='POST':
        leilao.delete()
        return redirect('catalogo:lista_leilao')
    return render(request, template_name, {'object':leilao})

@login_required
@comprador_required
def faz_lance(request, id_leilao, template_name='catalogo/lance_form.html'):
    form = LanceForm(request.POST or None, leilao=get_object_or_404(Leilao, pk=id_leilao))
    if form.is_valid():
        lance = form.save(commit=False)
        leilao = get_object_or_404(Leilao, pk=id_leilao)
        lance.leilao = leilao
        lance.comprador = request.user
        lance.save()
        return redirect('catalogo:detalha_leilao', pk=id_leilao)
    return render(request, template_name, {'form':form})

@login_required
@leiloeiro_required
def gera_relatorio(request, id_leilao, template_name='catalogo/gera_relatorio.html'):

    data = {}
    data['leilao_id'] = id_leilao

    return render(request, template_name, data)

@login_required
@leiloeiro_required
def gera_relatorio_desempenho(request, id_leilao, template_name='catalogo/gera_relatorio_desempenho.html'):
    leilao= get_object_or_404(Leilao, pk=id_leilao)

    lista_de_lances = list(Lance.objects.filter(leilao__id=id_leilao))

    data = {}
    data['leilao'] = leilao
    data['lance_vencedor'] = sorted(lista_de_lances, key=lambda t: t.valor, reverse=True)[0] if lista_de_lances else None
    data['total_de_lances'] = len(lista_de_lances)
    data['lance_inicial'] = lista_de_lances[0] if lista_de_lances else 'Não houve lances.'
    data['lance_final'] = lista_de_lances[-1] if lista_de_lances else 'Não houve lances.'
    data['status'] = 'Finalizado com sucesso.' if leilao.status == 'F' else 'Cancelado.'

    return render(request, template_name, data)


@login_required
@leiloeiro_required
def gera_relatorio_faturamento(request, id_leilao, template_name='catalogo/gera_relatorio_faturamento.html'):
    leilao= get_object_or_404(Leilao, pk=id_leilao)

    lista_de_lances = list(Lance.objects.filter(leilao__id=id_leilao))

    data = {}
    data['leilao'] = leilao
    data['lance_vencedor'] = sorted(lista_de_lances, key=lambda t: t.valor, reverse=True)[0] if lista_de_lances else None
    data['comissao_comprador'] = data['lance_vencedor'].valor * leilao.lote.taxa_de_comissao if leilao.status == 'F' else None
    data['comissao_vendedor'] = leilao.lote.valor_minimo_de_reserva * leilao.lote.taxa_de_comissao

    data['status'] = 'Finalizado com sucesso.' if leilao.status == 'F' else 'Cancelado.'

    return render(request, template_name, data)

@login_required
@leiloeiro_required
def gera_relatorio_desempenho_geral(request, template_name='catalogo/gera_relatorio_desempenho_geral.html'):

    data = {}
    data['leiloes_totais'] = len(list(Leilao.objects.all()))
    data['lotes_totais'] = len(list(Lance.objects.all()))
    data['lances_totais'] = len(list(Lote.objects.all()))
    data['usuarios_cadastrados'] = len(list(CustomUser.objects.all()))

    data['leiloes_ativos'] = len(list(Leilao.objects.filter(status='A')))
    data['leiloas_cancelados'] = len(list(Leilao.objects.filter(status='C')))
    data['leiloes_finalizados'] = len(list(Leilao.objects.filter(status='F')))
    data['leiloes_nao_iniciados'] = len(list(Leilao.objects.filter(status='N')))

    return render(request, template_name, data)

@login_required
@leiloeiro_required
def gera_relatorio_faturamento_geral(request, template_name='catalogo/gera_relatorio_faturamento_geral.html'):
    leiloes_finalizados = list(Leilao.objects.filter(status='F'))
    lotes_pagos = list(Lote.objects.filter(pago=1))

    data = {}
    data['faturamento_total'] = 0
    data['comissoes_pagas_por_compradores'] = 0
    data['comissoes_pagas_por_vendedores'] = 0
    data['valor_total_de_lances'] = 0

    for leilao in leiloes_finalizados:
        lista_de_lances = sorted(Lance.objects.filter(leilao_id = leilao.id), key=lambda t: t.valor, reverse=True)
        maior_lance = lista_de_lances[0] if lista_de_lances else None

        if maior_lance.valor <= 1000:
            taxa_de_comissao = 1/100
        elif maior_lance.valor <= 10000:
            taxa_de_comissao = 2/100
        elif maior_lance.valor <= 50000:
            taxa_de_comissao = 3/100
        elif maior_lance.valor <= 100000:
            taxa_de_comissao = 4/100
        else:
            taxa_de_comissao = 5/100

        data['comissoes_pagas_por_compradores'] += maior_lance.valor * taxa_de_comissao
    
    for lote in lotes_pagos:
        data['comissoes_pagas_por_vendedores'] += lote.valor_minimo_de_reserva * lote.taxa_de_comissao

    data['faturamento_total'] = data['comissoes_pagas_por_compradores'] + data['comissoes_pagas_por_vendedores']
        
    return render(request, template_name, data)

def gera_relatorio_pdf_desempenho_geral(request, template_name='catalogo/gera_relatorio_desempenho_geral.html'):
    leiloes_finalizados = list(Leilao.objects.filter(status='F'))

    data = {}
    data['leiloes_totais'] = len(list(Leilao.objects.all()))
    data['lotes_totais'] = len(list(Lance.objects.all()))
    data['lances_totais'] = len(list(Lote.objects.all()))
    data['usuarios_cadastrados'] = len(list(CustomUser.objects.all()))

    data['leiloes_ativos'] = len(list(Leilao.objects.filter(status='A')))
    data['leiloas_cancelados'] = len(list(Leilao.objects.filter(status='C')))
    data['leiloes_finalizados'] = len(list(Leilao.objects.filter(status='F')))
    data['leiloes_nao_iniciados'] = len(list(Leilao.objects.filter(status='N')))

    pdf = render_to_pdf(template_name, data)
    return HttpResponse(pdf, content_type='application/pdf')

def gera_relatorio_pdf_faturamento_geral(request, template_name='catalogo/gera_relatorio_faturamento_geral.html'):
    leiloes_finalizados = list(Leilao.objects.filter(status='F'))
    lotes_pagos = list(Lote.objects.filter(pago=1))

    data = {}
    data['faturamento_total'] = 0
    data['comissoes_pagas_por_compradores'] = 0
    data['comissoes_pagas_por_vendedores'] = 0
    data['valor_total_de_lances'] = 0

    for leilao in leiloes_finalizados:
        lista_de_lances = sorted(Lance.objects.filter(leilao_id = leilao.id), key=lambda t: t.valor, reverse=True)
        maior_lance = lista_de_lances[0] if lista_de_lances else None

        if maior_lance.valor <= 1000:
            taxa_de_comissao = 1/100
        elif maior_lance.valor <= 10000:
            taxa_de_comissao = 2/100
        elif maior_lance.valor <= 50000:
            taxa_de_comissao = 3/100
        elif maior_lance.valor <= 100000:
            taxa_de_comissao = 4/100
        else:
            taxa_de_comissao = 5/100

        data['comissoes_pagas_por_compradores'] += maior_lance.valor * taxa_de_comissao
    
    for lote in lotes_pagos:
        data['comissoes_pagas_por_vendedores'] += lote.valor_minimo_de_reserva * lote.taxa_de_comissao

    data['faturamento_total'] = data['comissoes_pagas_por_compradores'] + data['comissoes_pagas_por_vendedores']
    pdf = render_to_pdf(template_name, data)
    return HttpResponse(pdf, content_type='application/pdf')

