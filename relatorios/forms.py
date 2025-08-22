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
from .validators import validate_cpf, validate_cnpj, validate_phone, validate_cep, clean_cpf, clean_cnpj, clean_phone, clean_cep


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
        if not self.template or not ordem:
            return ordem
            
        # Check if position is already taken
        existing_query = ItemTabloide.objects.filter(
            template=self.template, 
            ordem=ordem
        )
        
        # Exclude current instance if we're editing
        if self.instance and self.instance.pk:
            existing_query = existing_query.exclude(pk=self.instance.pk)
            
        existing_item = existing_query.first()
        
        if existing_item:
            raise forms.ValidationError(
                f'❌ A posição {ordem} já está ocupada pelo produto "{existing_item.produto.nome}". '
                f'Escolha uma posição diferente ou remova o item existente primeiro.'
            )
        
        # Check if position is within template grid
        max_positions = self.template.colunas * self.template.linhas
        if ordem > max_positions or ordem < 1:
            raise forms.ValidationError(
                f'❌ A posição deve estar entre 1 e {max_positions}. '
                f'Este template tem dimensões {self.template.colunas}×{self.template.linhas} '
                f'(total de {max_positions} posições disponíveis).'
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
        widgets = {
            'razao_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razão Social da empresa'
            }),
            'nome_fantasia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome Fantasia (opcional)'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
                'data-mask': 'cnpj'
            }),
            'ie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inscrição Estadual'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'empresa@exemplo.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'data-mask': 'telefone'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'data-mask': 'cep'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }),
            'uf': forms.Select(choices=[
                ('', 'Selecione o Estado'),
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
                ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
                ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
                ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
            ], attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            cnpj = clean_cnpj(cnpj)
            validate_cnpj(cnpj)
        return cnpj
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone = clean_phone(telefone)
            validate_phone(telefone)
        return telefone
    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            cep = clean_cep(cep)
            validate_cep(cep)
        return cep


# Formulários de autenticação personalizados
class EmpresaSignUpForm(UserCreationForm):
    razao_social = forms.CharField(
        max_length=200, 
        required=True, 
        label="Razão Social",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Razão Social da empresa'
        })
    )
    nome_fantasia = forms.CharField(
        max_length=200, 
        required=False, 
        label="Nome Fantasia",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome Fantasia (opcional)'
        })
    )
    cnpj = forms.CharField(
        max_length=18, 
        required=True, 
        label="CNPJ",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00.000.000/0000-00',
            'data-mask': 'cnpj'
        })
    )
    ie = forms.CharField(
        max_length=20, 
        required=False, 
        label="Inscrição Estadual",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Inscrição Estadual'
        })
    )
    telefone = forms.CharField(
        max_length=30, 
        required=False, 
        label="Telefone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000',
            'data-mask': 'telefone'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de usuário da empresa"
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].label = "E-mail"
        self.fields['email'].help_text = "Este e-mail será usado para login e comunicações"
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            cnpj = clean_cnpj(cnpj)
            validate_cnpj(cnpj)
        return cnpj
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone = clean_phone(telefone)
            validate_phone(telefone)
        return telefone


class ClienteSignUpForm(UserCreationForm):
    nome_completo = forms.CharField(
        max_length=200, 
        required=True, 
        label="Nome Completo",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome completo do cliente'
        })
    )
    telefone = forms.CharField(
        max_length=30, 
        required=False, 
        label="Telefone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000',
            'data-mask': 'telefone'
        })
    )
    cpf = forms.CharField(
        max_length=14, 
        required=False, 
        label="CPF",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'data-mask': 'cpf'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de usuário"
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].label = "E-mail"
        self.fields['email'].help_text = "Este e-mail será usado para login e comunicações"
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = clean_cpf(cpf)
            validate_cpf(cpf)
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone = clean_phone(telefone)
            validate_phone(telefone)
        return telefone


class ClienteForm(forms.ModelForm):
    class Meta:
        model = UsuarioCliente
        fields = [
            "nome_completo",
            "telefone",
            "cpf",
            "empresa_associada",
        ]
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do cliente'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'data-mask': 'telefone'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'data-mask': 'cpf'
            }),
            'empresa_associada': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = clean_cpf(cpf)
            validate_cpf(cpf)
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone = clean_phone(telefone)
            validate_phone(telefone)
        return telefone
