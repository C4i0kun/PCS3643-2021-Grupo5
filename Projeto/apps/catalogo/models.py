from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings

class CustomUser(User):
    TIPO_USUARIO_CHOICES = (
        ("C", "Comprador"),
        ("L", "Leiloeiro"),
        ("V", "Vendedor")
    )

    tipo_usuario = models.CharField(max_length=1, choices=TIPO_USUARIO_CHOICES, blank=False, null=False)

# class Comprador(models.Model):
#     usuario = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.usuario

# class Leiloeiro(models.Model):
#     usuario = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.usuario

# class Vendedor(models.Model):
#     usuario = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.usuario

class Lote(models.Model):
    ESTADO_CHOICES = (
        ("N", "Novo"),
        ("S", "Seminovo"),
        ("U", "Usado")
    )

    ESTADO_DICT = {"N": "Novo", "S": "Seminovo", "U": "Usado"}

    name = models.CharField(max_length=200, verbose_name='Nome do Lote')
    descricao = models.CharField(max_length=1000, verbose_name='Descrição dos Itens do Lote')
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, blank=False, null=False, verbose_name='Estado do Lote')
    taxa_de_comissao = models.FloatField()
    valor_minimo_de_lote = models.FloatField(verbose_name='Valor Inicial do Lote')
    valor_minimo_de_reserva = models.FloatField(verbose_name='Valor Mínimo de Reserva')
    valor_minimo_por_lance = models.FloatField(verbose_name='Valor Mínimo por Lance')

    pago = models.BooleanField()

    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogo:detalha_lote', kwargs={'pk': self.pk})

class Leilao(models.Model):
    STATUS_CHOICES = (
        ("N", "Não iniciado"),
        ("A", "Ativo"),
        ("C", "Cancelado"),
        ("F", "Finalizado")
    )

    STATUS_DICT = {"N": "Não iniciado", "A": "Ativo", "C": "Cancelado", "F": "Finalizado"}

    name = models.CharField(max_length=200, verbose_name='Nome do Leilão')
    periodoInicio = models.DateTimeField(verbose_name='Dia e Horário de Início do Leilão')
    periodoFinal = models.DateTimeField(verbose_name='Dia e Horário de Encerramento do Leilão')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=False, null=False)

    pago = models.BooleanField()

    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogo:detalha_leilao', kwargs={'pk': self.pk})

class Lance(models.Model):
    valor = models.FloatField(verbose_name='Valor do Lance')

    comprador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leilao = models.ForeignKey(Leilao, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - R${1}'.format(self.comprador.username, self.valor)