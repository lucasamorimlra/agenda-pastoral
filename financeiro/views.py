from django.shortcuts import render
from django.utils import timezone

from .services import calcular_balanco

MESES = [
    (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
    (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
    (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
]


def _periodo_da_requisicao(request):
    hoje = timezone.localdate()
    try:
        ano = int(request.GET.get('ano', hoje.year))
        mes = int(request.GET.get('mes', hoje.month))
    except ValueError:
        return hoje.year, hoje.month

    if not (1 <= mes <= 12 and 2000 <= ano <= 2100):
        return hoje.year, hoje.month
    return ano, mes


def index(request):
    ano, mes = _periodo_da_requisicao(request)

    contexto = calcular_balanco(ano, mes)
    contexto.update({
        'ano': ano,
        'mes': mes,
        'nome_mes': dict(MESES)[mes],
        'meses': MESES,
    })
    return render(request, 'financeiro/index.html', contexto)