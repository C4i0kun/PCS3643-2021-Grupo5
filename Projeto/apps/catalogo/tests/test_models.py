from django.test import TestCase
from datetime import datetime, timezone, timedelta
import pytz

# Create your tests here.

from ..models import Vendedor, Comprador, Lote, Leilao, Lance
from django.contrib.auth.models import User

class VendedorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Vendedor.objects.create(name='Caio')

    def test_name_label(self):
        vendedor = Vendedor.objects.get(id=1)
        field_label = vendedor._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Nome')

    def test_name_max_length(self):
        vendedor = Vendedor.objects.get(id=1)
        max_length = vendedor._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_criacao_de_nome(self):
        vendedor = Vendedor.objects.get(id=1)

        self.assertEquals(vendedor.name, 'Caio')

    def test_nome_do_objeto(self):
        vendedor = Vendedor.objects.get(id=1)
        expected_object_name = vendedor.name

        self.assertEquals(str(vendedor), expected_object_name)

class CompradorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Comprador.objects.create(name='Caio')

    def test_name_label(self):
        comprador = Comprador.objects.get(id=1)
        field_label = comprador._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Nome')

    def test_name_max_length(self):
        comprador = Comprador.objects.get(id=1)
        max_length = comprador._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_criacao_de_nome(self):
        comprador = Comprador.objects.get(id=1)

        self.assertEquals(comprador.name, 'Caio')

    def test_nome_do_objeto(self):
        comprador = Comprador.objects.get(id=1)
        expected_object_name = comprador.name

        self.assertEquals(str(comprador), expected_object_name)

class LoteModelTest(TestCase):

    @classmethod
    def setUp(self):
        """Set up non-modified objects used by all test methods."""
        self.usuario_vendedor = User.objects.create_user(username='caio', password='caio123')

        self.lote = Lote.objects.create(name="Lote do Caio", descricao="Artigos do Caio",
                            estado="N", valor_minimo_de_lote=1000, taxa_de_comissao=1/100,
                            valor_minimo_de_reserva=2000, valor_minimo_por_lance=200,
                            vendedor=self.usuario_vendedor)

    def test_nome_do_objeto(self):
        """Testa se o nome do lote é o nome do objeto."""
        lote = self.lote
        expected_object_name = lote.name

        self.assertEquals(str(lote), expected_object_name)

    def test_get_absolute_url(self):
        """Testa a url do lote."""
        lote = self.lote
        # This will also fail if the urlconf is not defined.
        self.assertEquals(lote.get_absolute_url(), '/catalogo/lote/{}/'.format(lote.id))

    def test_vendedor_cadastrado(self):
        """Testa se o usuário cadastrado como vendedor está correto."""
        lote = self.lote
        usuario_vendedor = self.usuario_vendedor

        self.assertEquals(lote.vendedor, usuario_vendedor)

class LeilaoModelTest(TestCase):

    @classmethod
    def setUp(self):
        """Set up non-modified objects used by all test methods."""
        self.usuario_vendedor = User.objects.create_user(username='caio', password='caio123')

        self.lote = Lote.objects.create(name="Lote do Caio", descricao="Artigos do Caio",
                                   estado="N", valor_minimo_de_lote=1000, taxa_de_comissao=1/100,
                                   valor_minimo_de_reserva=2000, valor_minimo_por_lance=200,
                                   vendedor=self.usuario_vendedor)

        self.leilao = Leilao.objects.create(name="Leilão do Caio", 
                              periodoInicio=datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(hours=1),
                              periodoFinal=datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=3),
                              lote=self.lote)

    def test_nome_do_objeto(self):
        """Testa se o nome do leilao é o nome do objeto."""
        leilao = self.leilao
        expected_object_name = leilao.name

        self.assertEquals(str(leilao), expected_object_name)

    def test_get_absolute_url(self):
        """Testa a url do leilao."""
        leilao = self.leilao
        # This will also fail if the urlconf is not defined.
        self.assertEquals(leilao.get_absolute_url(), '/catalogo/leilao/{}/'.format(leilao.id))

    def test_lote_referente(self):
        """Testa se o lote referente ao leilão está correto."""
        leilao = self.leilao
        lote = self.lote

        self.assertEquals(leilao.lote, lote)

class LanceModelTest(TestCase):

    @classmethod
    def setUp(self):
        """Set up non-modified objects used by all test methods."""
        self.usuario_vendedor = User.objects.create_user(username='caio', password='caio123')
        self.usuario_comprador = User.objects.create_user(username='bernardo', password='bernardo123')

        self.lote = Lote.objects.create(name="Lote do Caio", descricao="Artigos do Caio",
                                   estado="N", valor_minimo_de_lote=1000, taxa_de_comissao=1/100,
                                   valor_minimo_de_reserva=2000, valor_minimo_por_lance=200,
                                   vendedor=self.usuario_vendedor)

        self.leilao = Leilao.objects.create(name="Leilão do Caio", 
                              periodoInicio=datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(hours=1),
                              periodoFinal=datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=3),
                              lote=self.lote)

        self.lance = Lance.objects.create(valor=2199.99, comprador=self.usuario_comprador, leilao=self.leilao)

    def test_nome_do_objeto(self):
        """Testa se o nome do lance é o nome do objeto."""
        lance = self.lance
        expected_object_name = '{0}: R${1}'.format(self.usuario_comprador.username, lance.valor)
        
        self.assertEquals(str(lance), expected_object_name)

    def test_valor_do_objeto(self):
        """Testa se o valor do lance é o valor correto."""
        lance = self.lance
        valor_esperado = 2199.99

        self.assertEquals(lance.valor, valor_esperado)

    def test_usuario_comprador_referente(self):
        """Testa se o usuário comprador referente ao lance está correto."""
        lance = self.lance
        usuario_comprador = self.usuario_comprador

        self.assertEquals(lance.comprador, usuario_comprador)

    def test_leilao_referente(self):
        """Testa se o leilão referente ao lance está correto."""
        lance = self.lance
        leilao = self.leilao

        self.assertEquals(lance.leilao, leilao)
