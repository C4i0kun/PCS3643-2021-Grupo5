from .models import CustomUser, Leilao, Lance
from datetime import datetime, timezone
import pytz

def encerra_leilao(leilao):
    lista_de_lances = list(Lance.objects.filter(leilao_id = leilao.id))

    maior_lance = 0

    if lista_de_lances:
        maior_lance = sorted(lista_de_lances, key=lambda t: t.valor, reverse=True)[0].valor
    
    if len(lista_de_lances) > 0 and maior_lance >= leilao.lote.valor_minimo_de_reserva:
        leilao.status = 'F'
    else:
        leilao.status = 'C'

    leilao.save()

def checa_status_leiloes():
    ## Checa se leiloes devem ser iniciados
    leiloes_para_checar = list(Leilao.objects.filter(status = 'N') | Leilao.objects.filter(status = 'A'))
    for leilao in leiloes_para_checar:
        if leilao.status == 'N' and datetime.now(pytz.timezone('America/Sao_Paulo')).replace(tzinfo=pytz.timezone('America/Sao_Paulo')) > leilao.periodoInicio.replace(tzinfo=pytz.timezone('America/Sao_Paulo')):
            leilao.status = 'A'
            leilao.save()

        if leilao.status == 'A' and datetime.now(pytz.timezone('America/Sao_Paulo')).replace(tzinfo=pytz.timezone('America/Sao_Paulo')) > leilao.periodoFinal.replace(tzinfo=pytz.timezone('America/Sao_Paulo')):
            encerra_leilao(leilao)    
    

def cria_usuarios():
    if not CustomUser.objects.filter(username='usuario_comprador').exists():
        user=CustomUser.objects.create_user('usuario_comprador', password='senha')
        user.is_superuser=False
        user.is_staff=False
        user.tipo_usuario='C'
        user.save()

    if not CustomUser.objects.filter(username='usuario_vendedor').exists():
        user=CustomUser.objects.create_user('usuario_vendedor', password='senha')
        user.is_superuser=False
        user.is_staff=False
        user.tipo_usuario='V'
        user.save()

    if not CustomUser.objects.filter(username='usuario_leiloeiro').exists():
        user=CustomUser.objects.create_user('usuario_leiloeiro', password='senha')
        user.is_superuser=False
        user.is_staff=False
        user.tipo_usuario='L'
        user.save()