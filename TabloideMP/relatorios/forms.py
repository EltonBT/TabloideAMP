from django import forms

from .models import (
    Produto,
    TabelaPrecoImportacao,
    TemplateTabloide,
    ItemTabloide,
    ThemeSettings,
    Empresa,
)


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "codigo",
            "codigo_barras",
            "nome",
            "descricao",
            "preco",
            "imagem",
        ]


class ImportacaoTabelaForm(forms.ModelForm):
    class Meta:
        model = TabelaPrecoImportacao
        fields = ["arquivo"]


class TemplateTabloideForm(forms.ModelForm):
    class Meta:
        model = TemplateTabloide
        fields = ["nome", "colunas", "linhas", "cor_fundo_row", "background_imagem"]


class ItemTabloideForm(forms.ModelForm):
    class Meta:
        model = ItemTabloide
        fields = ["template", "produto", "ordem"]


class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = ThemeSettings
        fields = [
            "is_active",
            "dark_bg",
            "dark_card",
            "dark_text",
            "dark_muted",
            "dark_brand",
            "light_bg",
            "light_card",
            "light_text",
            "light_muted",
            "light_brand",
        ]


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "ie",
            "email",
            "telefone",
            "cep",
            "endereco",
            "cidade",
            "uf",
            "logo",
        ]
