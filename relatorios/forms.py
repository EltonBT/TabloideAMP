from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    Produto,
    TabelaPrecoImportacao,
    TemplateTabloide,
    ItemTabloide,
    ThemeSettings,
    Empresa,
    UsuarioCliente,
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
        fields = ["nome", "colunas", "linhas", "cor_fundo_row", "cor_fundo_alternada", "background_imagem"]


class TemplateTabloideEditForm(forms.ModelForm):
    class Meta:
        model = TemplateTabloide
        fields = ["nome", "colunas", "linhas", "cor_fundo_row", "cor_fundo_alternada", "background_imagem"]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do template'
            }),
            'colunas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '6'
            }),
            'linhas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '8'
            }),
            'cor_fundo_row': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control color-input',
                'data-preview': 'primary'
            }),
            'cor_fundo_alternada': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control color-input',
                'data-preview': 'alternate'
            }),
            'background_imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class ItemTabloideForm(forms.ModelForm):
    class Meta:
        model = ItemTabloide
        fields = ["produto", "ordem"]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Posição (1, 2, 3...)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop('template', None)
        super().__init__(*args, **kwargs)
        if self.template:
            self.fields['produto'].queryset = Produto.objects.exclude(
                itemtabloide__template=self.template
            )
    
    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if self.template and ordem:
            # Check if position is already taken
            existing_item = ItemTabloide.objects.filter(
                template=self.template, 
                ordem=ordem
            ).exclude(pk=self.instance.pk if self.instance.pk else None)
            
            if existing_item.exists():
                raise forms.ValidationError(f'A posição {ordem} já está ocupada por outro item.')
            
            # Check if position is within template grid
            max_positions = self.template.colunas * self.template.linhas
            if ordem > max_positions:
                raise forms.ValidationError(
                    f'A posição deve estar entre 1 e {max_positions} '
                    f'(grid de {self.template.colunas}x{self.template.linhas}).'
                )
        return ordem
    
    def save(self, commit=True):
        item = super().save(commit=False)
        if self.template:
            item.template = self.template
        if commit:
            item.save()
        return item


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


# Formulários de autenticação personalizados
class EmpresaSignUpForm(UserCreationForm):
    razao_social = forms.CharField(max_length=200, required=True, label="Razão Social")
    nome_fantasia = forms.CharField(max_length=200, required=False, label="Nome Fantasia")
    cnpj = forms.CharField(max_length=18, required=True, label="CNPJ")
    ie = forms.CharField(max_length=20, required=False, label="Inscrição Estadual")
    email = forms.EmailField(required=True, label="E-mail")
    telefone = forms.CharField(max_length=30, required=False, label="Telefone")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de usuário da empresa"
        self.fields['email'].help_text = "Este e-mail será usado para login e comunicações"


class ClienteSignUpForm(UserCreationForm):
    nome_completo = forms.CharField(max_length=200, required=True, label="Nome Completo")
    telefone = forms.CharField(max_length=30, required=False, label="Telefone")
    cpf = forms.CharField(max_length=14, required=False, label="CPF")
    email = forms.EmailField(required=True, label="E-mail")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de usuário"
        self.fields['email'].help_text = "Este e-mail será usado para login e comunicações"
