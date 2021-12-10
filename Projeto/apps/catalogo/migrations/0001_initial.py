# Generated by Django 2.0.5 on 2018-05-11 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.auth.models import User
from ..models import Leilao, Lote

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    TIPO_USUARIO_CHOICES = (
        ("C", "Comprador"),
        ("L", "Leiloeiro"),
        ("V", "Vendedor")
    )

    ESTADO_LOTE_CHOICES = (
        ("N", "Novo"),
        ("S", "Seminovo"),
        ("U", "Usado")
    )

    STATUS_LEILAO_CHOICES = (
        ("N", "Não iniciado"),
        ("A", "Ativo"),
        ("F", "Finalizado")
    )

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('tipo_usuario', models.CharField(choices=TIPO_USUARIO_CHOICES, max_length=1)),
            ],
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ]
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descricao', models.CharField(max_length=1000)),
                ('estado', models.CharField(max_length=1, choices=ESTADO_LOTE_CHOICES, blank=False, null=False)),
                ('taxa_de_comissao', models.FloatField()),
                ('valor_minimo_de_lote', models.FloatField()),
                ('valor_minimo_de_reserva', models.FloatField()),
                ('valor_minimo_por_lance', models.FloatField()),
                ('pago', models.BooleanField()),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leilao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('periodoInicio', models.DateTimeField()),
                ('periodoFinal', models.DateTimeField()),
                ('status',  models.CharField(max_length=1, choices=STATUS_LEILAO_CHOICES, blank=False, null=False)),
                ('pago', models.BooleanField()),
                ('lote', models.ForeignKey(to='Lote', on_delete=models.CASCADE))
            ],
        ),
        migrations.CreateModel(
            name='Lance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('leilao', models.ForeignKey(to='Leilao', on_delete=models.CASCADE))
            ],
        ),
    ]