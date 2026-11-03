from datetime import date
from decimal import Decimal

from django.db.models import Sum

from .models import Movimentacao, TipoMovimento


def _soma(queryset, tipo):
    total = queryset.filter(tipo=tipo).aggregate(total=Sum('valor'))['total']
    return total or Decimal('0.00')


def calcular_balanco(ano, mes):
    inicio_do_mes = date(ano, mes, 1)

    anteriores = Movimentacao.objects.filter(data__lt=inicio_do_mes)
    saldo_anterior = (
        _soma(anteriores, TipoMovimento.RECEITA)
        - _soma(anteriores, TipoMovimento.DESPESA)
    )

    movimentacoes = (
        Movimentacao.objects
        .filter(data__year=ano, data__month=mes)
        .select_related('categoria')
    )
    total_entradas = _soma(movimentacoes, TipoMovimento.RECEITA)
    total_saidas = _soma(movimentacoes, TipoMovimento.DESPESA)

    return {
        'movimentacoes': movimentacoes,
        'saldo_anterior': saldo_anterior,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_atual': saldo_anterior + total_entradas - total_saidas,
    }