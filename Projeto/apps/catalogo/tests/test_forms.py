from django.test import TestCase

# Create your tests here.

from datetime import datetime, timezone, timedelta
import pytz
from ..views import LoteForm, LeilaoForm, LanceForm
from ..models import Lote, Leilao, Lance
from django.contrib.auth.models import User

class LanceFormTest(TestCase):
    @classmethod
    def setUp(self):
        self.usuario_vendedor = User.objects.create_user(username='caio', password='caio123')
        self.lote = Lote.objects.create(name="lote_lance", descricao="teste",
                            estado="N", valor_minimo_de_lote=1000, taxa_de_comissao=1/100,
                            valor_minimo_de_reserva=2000, valor_minimo_por_lance=200,
                            vendedor=self.usuario_vendedor, pago=False)
        self.leilao = Leilao.objects.create(name="leilao_lance",
                            periodoInicio=datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(hours=1),
                            periodoFinal=datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=3),
                            pago=False, lote=self.lote)

    def test_valor_igual_a_zero(self):
        """Test form é inválido se o valor é igual a zero."""
        form = LanceForm(data={'valor': 0}, leilao=self.leilao)
        self.assertFalse(form.is_valid())

    def test_valor_menor(self):
        """Test form é inválido se o valor é menor do que o valor de lote."""
        form = LanceForm(data={'valor': 999}, leilao=self.leilao)
        self.assertFalse(form.is_valid())

    def test_valor_minimo(self):
        """Test form é válido se o valor é igual ao valor de lote."""
        form = LanceForm(data={'valor': 1000}, leilao=self.leilao)
        self.assertTrue(form.is_valid())

    def test_valor_field_label(self):
        """A label de valor é 'Valor'."""
        form = LanceForm(data={'valor': 1}, leilao=self.leilao)
        self.assertTrue(
            form.fields['valor'].label is None or
            form.fields['valor'].label == 'Valor do Lance')

class LeilaoFormTest(TestCase):

    def test_periodoInicio_sem_horario(self):
        """Testa se o form é inválido caso o início do periódo do leilão for no passado."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': 'errado',
            'periodoFinal': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_periodoFinal_sem_horario(self):
        """Testa se o form é inválido caso o início do periódo do leilão for no passado."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=2),
            'periodoFinal': 'errado'})
        self.assertFalse(form.is_valid())

    def test_periodoInicio_anterior_ao_horario_atual(self):
        """Testa se o form é inválido caso o início do periódo do leilão for no passado."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(pytz.timezone('America/Sao_Paulo')) - timedelta(hours=1),
            'periodoFinal': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_periodoInicio_apos_periodoFinal(self):
        """Testa se o form é inválido caso o início do período seja posterior ao seu fim."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=2),
            'periodoFinal': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_periodoInicio_valido(self):
        """Testa se um período de início é válido."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(hours=1),
            'periodoFinal': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=3)})
        self.assertTrue(form.is_valid())

    def test_periodoFinal_anterior_ao_horario_atual(self):
        """Testa se o form é inválido caso o fim do período do leilão for no passado."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(pytz.timezone('America/Sao_Paulo')),
            'periodoFinal': datetime.now(pytz.timezone('America/Sao_Paulo')) - timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_periodoFinal_anterior_ao_horario_atual_mais_um_dia(self):
        """Testa se o form é inválido caso o fim do período seja anterior ao horário atual mais um dia."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(pytz.timezone('America/Sao_Paulo')),
            'periodoFinal': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(hours=18)})
        self.assertFalse(form.is_valid())

    def test_periodoFinal_anterior_ao_periodoInicio_mais_um_dia(self):
        """Testa se o form é inválido caso o fim do período seja anterior ao seu início mais um dia."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=2),
            'periodoFinal': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=1)})
        self.assertFalse(form.is_valid())


    def test_periodoFinal_valido(self):
        """Testa se um período final é válido."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(hours=1),
            'periodoFinal': datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(days=3)})
        self.assertTrue(form.is_valid())

class LoteFormTest(TestCase):

    def test_valor_minimo_de_reserva_nulo(self):
        """Testa se o valor mínimo de reserva é inválido se for menor ou igual a zero"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': 0,
            'valor_minimo_de_reserva': 0,
            'valor_minimo_por_lance': 50})
        self.assertFalse(form.is_valid())

    def test_valor_minimo_de_reserva_negativo(self):
        """Testa se o valor mínimo de reserva é inválido se for menor ou igual a zero"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': 0,
            'valor_minimo_de_reserva': -30,
            'valor_minimo_por_lance': 50})
        self.assertFalse(form.is_valid())

    def test_valores_validos(self):
        """Testa se o valor mínimo de reserva, de lote e por lance são válidos"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_reserva': 100})
        self.assertTrue(form.is_valid())

    def test_outros_valores_validos(self):
        """Testa se o valor mínimo de reserva, de lote e por lance são válidos"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_reserva': 2549.90})
        self.assertTrue(form.is_valid())