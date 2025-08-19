from django.contrib import admin

from .models import (
    Produto,
    TabelaPrecoImportacao,
    TemplateTabloide,
    ItemTabloide,
    ThemeSettings,
    Empresa,
)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "preco")
    search_fields = ("codigo", "codigo_barras", "nome")
    list_filter = ("atualizado_em",)


@admin.register(TabelaPrecoImportacao)
class TabelaPrecoImportacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "arquivo", "processado", "criado_em")
    list_filter = ("processado", "criado_em")


class ItemTabloideInline(admin.TabularInline):
    model = ItemTabloide
    extra = 1


@admin.register(TemplateTabloide)
class TemplateTabloideAdmin(admin.ModelAdmin):
    list_display = ("nome", "colunas", "linhas", "cor_fundo_row")
    inlines = [ItemTabloideInline]


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "cnpj", "cidade", "uf")
    search_fields = ("razao_social", "nome_fantasia", "cnpj")


# Register your models here.
