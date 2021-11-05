from django.test import TestCase

# Create your tests here.

from datetime import datetime, timezone, timedelta
from ..views import LoteForm, LeilaoForm, LanceForm

class LanceFormTest(TestCase):

    def test_valor_igual_a_zero(self):
        """Test form é inválido se o valor é igual a zero."""
        form = LanceForm(data={'valor': 0})
        self.assertFalse(form.is_valid())

    def test_valor_minimo(self):
        """Test form é válido se o valor é igual a um."""
        form = LanceForm(data={'valor': 1})
        self.assertTrue(form.is_valid())

    def test_valor_field_label(self):
        """A label de valor é 'Valor'."""
        form = LanceForm()
        self.assertTrue(
            form.fields['valor'].label is None or
            form.fields['valor'].label == 'Valor')

class LeilaoFormTest(TestCase):

    def test_periodoInicio_anterior_ao_horario_atual(self):
        """Testa se o form é inválido caso o início do periódo do leilão for no passado."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now() - timedelta(hours=1),
            'periodoFinal': datetime.now() + timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_periodoInicio_apos_periodoFinal(self):
        """Testa se o form é inválido caso o início do período seja posterior ao seu fim."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now() + timedelta(days=2),
            'periodoFinal': datetime.now() + timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_periodoInicio_valido(self):
        """Testa se um período de início é válido."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now() + timedelta(hours=10),
            'periodoFinal': datetime.now() + timedelta(days=3)})
        self.assertTrue(form.is_valid())

    def test_periodoFinal_anterior_ao_horario_atual(self):
        """Testa se o form é inválido caso o fim do período do leilão for no passado."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(),
            'periodoFinal': datetime.now() - timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_periodoFinal_anterior_ao_horario_atual_mais_um_dia(self):
        """Testa se o form é inválido caso o fim do período seja anterior ao horário atual mais um dia."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now(),
            'periodoFinal': datetime.now() + timedelta(hours=18)})
        self.assertFalse(form.is_valid())

    def test_periodoFinal_anterior_ao_periodoInicio_mais_um_dia(self):
        """Testa se o form é inválido caso o fim do período seja anterior ao seu início mais um dia."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now() + timedelta(days=2),
            'periodoFinal': datetime.now() + timedelta(days=1)})
        self.assertFalse(form.is_valid())


    def test_periodoFinal_valido(self):
        """Testa se um período final é válido."""
        form = LeilaoForm(data={
            'name' : 'Teste',
            'periodoInicio': datetime.now() + timedelta(hours=7),
            'periodoFinal': datetime.now() + timedelta(days=3)})
        self.assertTrue(form.is_valid())

class LoteFormTest(TestCase):

    def test_valor_minimo_de_lote_negativo(self):
        """Testa se o valor mínimo de lote é inválido se for menor que zero"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': -3,
            'valor_minimo_de_reserva': 100,
            'valor_minimo_por_lance': 50})
        self.assertFalse(form.is_valid())

    def test_valor_minimo_de_lote_nulo(self):
        """Testa se o valor mínimo de lote é inválido se for igual a zero"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': 0,
            'valor_minimo_de_reserva': 100,
            'valor_minimo_por_lance': 50})
        self.assertFalse(form.is_valid())

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

    def test_valor_minimo_de_reserva_menor_que_o_valor_minimo(self):
        """Testa se o valor mínimo de reserva é inválido se for menor que o valor mínimo"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': 100,
            'valor_minimo_de_reserva': 20,
            'valor_minimo_por_lance': 50})
        self.assertFalse(form.is_valid())

    def test_valor_minimo_de_lance_nulo(self):
        """Testa se o valor mínimo de lance é inválido se for nulo"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': 20,
            'valor_minimo_de_reserva': 100,
            'valor_minimo_por_lance': 0})
        self.assertFalse(form.is_valid())

    def test_valor_minimo_de_lance_negativo(self):
        """Testa se o valor mínimo de lance é inválido se for negativo"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': 20,
            'valor_minimo_de_reserva': 100,
            'valor_minimo_por_lance': -15})
        self.assertFalse(form.is_valid())

    def test_valores_validos(self):
        """Testa se o valor mínimo de reserva, de lote e por lance são válidos"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': 20,
            'valor_minimo_de_reserva': 100,
            'valor_minimo_por_lance': 50})
        self.assertTrue(form.is_valid())

    def test_outros_valores_validos(self):
        """Testa se o valor mínimo de reserva, de lote e por lance são válidos"""
        form = LoteForm(data={
            'name' : 'Lote do Bernardo',
            'descricao' : '1 (Um) Bernardo um pouco desgastado pela Poli',
            'estado' : 'U',
            'valor_minimo_de_lote': 199.9,
            'valor_minimo_de_reserva': 2549.90,
            'valor_minimo_por_lance': 10})
        self.assertTrue(form.is_valid())