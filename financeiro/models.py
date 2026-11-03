from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class TipoMovimento(models.TextChoices):
    RECEITA = 'R', 'Receita'
    DESPESA = 'D', 'Despesa'


class FormaPagamento(models.TextChoices):
    DINHEIRO = 'DIN', 'Dinheiro'
    PIX = 'PIX', 'Pix'
    TRANSFERENCIA = 'TED', 'Transferência'
    CARTAO = 'CAR', 'Cartão'
    CHEQUE = 'CHQ', 'Cheque'
    OUTRO = 'OUT', 'Outro'


class Categoria(models.Model):
    nome = models.CharField(max_length=80)
    tipo = models.CharField(max_length=1, choices=TipoMovimento.choices)

    class Meta:
        ordering = ['tipo', 'nome']

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'


class Movimentacao(models.Model):
    tipo = models.CharField(max_length=1, choices=TipoMovimento.choices)
    data = models.DateField()
    descricao = models.CharField('histórico', max_length=200)
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    forma_pagamento = models.CharField(
        max_length=3,
        choices=FormaPagamento.choices,
        default=FormaPagamento.DINHEIRO,
    )
    documento = models.CharField('nº do documento', max_length=30, blank=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data', 'id']
        verbose_name = 'movimentação'
        verbose_name_plural = 'movimentações'

    def __str__(self):
        return f'{self.data:%d/%m/%Y} - {self.descricao} - R$ {self.valor}'

    @property
    def eh_receita(self):
        return self.tipo == TipoMovimento.RECEITA