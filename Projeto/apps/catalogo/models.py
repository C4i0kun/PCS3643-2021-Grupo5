from django.db import models
from django.urls import reverse
from django.conf import settings

class Lote(models.Model):
    numero_sequencial = models.IntegerField() # Transformar em Index depois
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    descricao = models.CharField(max_length=1000)
    estado = models.CharField(max_length=20)
    taxa_de_comissao = models.FloatField()
    valor_minimo_de_lote = models.FloatField()
    valor_minimo_de_reserva = models.FloatField()
    valor_minimo_por_lance = models.FloatField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogo:atualiza_lote', kwargs={'pk': self.pk})