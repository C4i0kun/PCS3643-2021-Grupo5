from django.db import models
from django.urls import reverse
from django.conf import settings

class Vendedor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Comprador(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Lote(models.Model):
    name = models.CharField(max_length=200)
    numero_sequencial = models.IntegerField()
    descricao = models.CharField(max_length=1000)
    estado = models.CharField(max_length=20)
    taxa_de_comissao = models.FloatField()
    valor_minimo_de_lote = models.FloatField()
    valor_minimo_de_reserva = models.FloatField()
    valor_minimo_por_lance = models.FloatField()

    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogo:atualiza_lote', kwargs={'pk': self.pk})

class Leilao(models.Model):
    name = models.CharField(max_length=200)
    periodoInicio = models.DateTimeField()
    periodoFinal = models.DateTimeField()
    
    lote = models.OneToOneField(
        Lote,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogo:atualiza_leilao', kwargs={'pk': self.pk})

class Lance(models.Model):
    valor = models.FloatField()

    comprador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leilao = models.ForeignKey(Leilao, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.valor)