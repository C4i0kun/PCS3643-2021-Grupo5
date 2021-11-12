from django import template
from ..models import Lance

register = template.Library()

@register.filter
def pega_lances_de_leilao(lista_de_lances, id_leilao):
    return sorted(list(Lance.objects.filter(leilao__id=id_leilao)), key=lambda t: t.valor, reverse=True)