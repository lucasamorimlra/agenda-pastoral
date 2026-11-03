from django.contrib import admin

# Register your models here.
from .models import Categoria, Movimentacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo')
    list_filter = ('tipo',)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'descricao', 'tipo', 'categoria', 'valor', 'forma_pagamento')
    list_filter = ('tipo', 'categoria', 'forma_pagamento')
    search_fields = ('descricao', 'documento')
    date_hierarchy = 'data'