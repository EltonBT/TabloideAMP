from django.db import models
from django.contrib.auth.models import User


class Produto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    codigo_barras = models.CharField(max_length=64, blank=True, null=True, unique=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return f"{self.nome} ({self.codigo})"


class TabelaPrecoImportacao(models.Model):
    arquivo = models.FileField(upload_to="importacoes/")
    criado_em = models.DateTimeField(auto_now_add=True)
    processado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Importação #{self.id} - {self.arquivo.name}"


class TemplateTabloide(models.Model):
    nome = models.CharField(max_length=100)
    colunas = models.PositiveIntegerField(default=3)
    linhas = models.PositiveIntegerField(default=4)
    cor_fundo_row = models.CharField(max_length=7, default="#FFFFFF", verbose_name="Cor de fundo principal")  # HEX
    cor_fundo_alternada = models.CharField(
        max_length=7, default="#FFFFFF", blank=True, verbose_name="Cor de fundo alternada"
    )  # HEX para intercalado
    background_imagem = models.ImageField(
        upload_to="backgrounds/", blank=True, null=True
    )

    class Meta:
        verbose_name = "Template de Tabloide"
        verbose_name_plural = "Templates de Tabloide"

    def __str__(self) -> str:
        return self.nome


class ItemTabloide(models.Model):
    template = models.ForeignKey(
        TemplateTabloide, on_delete=models.CASCADE, related_name="itens"
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem"]
        unique_together = [("template", "produto"), ("template", "ordem")]

    def __str__(self) -> str:
        return f"{self.template.nome} - {self.produto.nome}"


class ThemeSettings(models.Model):
    name = models.CharField(max_length=50, default="default")
    is_active = models.BooleanField(default=True)

    # Dark theme
    dark_bg = models.CharField(max_length=7, default="#0b0c10")
    dark_card = models.CharField(max_length=7, default="#12141a")
    dark_text = models.CharField(max_length=7, default="#e6edf3")
    dark_muted = models.CharField(max_length=7, default="#9aa4b2")
    dark_brand = models.CharField(max_length=7, default="#7c3aed")

    # Light theme
    light_bg = models.CharField(max_length=7, default="#f7f7f8")
    light_card = models.CharField(max_length=7, default="#ffffff")
    light_text = models.CharField(max_length=7, default="#0b1220")
    light_muted = models.CharField(max_length=7, default="#4b5563")
    light_brand = models.CharField(max_length=7, default="#7c3aed")

    class Meta:
        verbose_name = "Configuração de Tema"
        verbose_name_plural = "Configurações de Tema"

    def __str__(self) -> str:
        return f"Tema: {self.name} ({'ativo' if self.is_active else 'inativo'})"


# Create your models here.


class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empresa_profile', null=True, blank=True)
    razao_social = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200, blank=True)
    cnpj = models.CharField(max_length=18, unique=True)
    ie = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    logo = models.ImageField(upload_to="empresas/", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["razao_social"]

    def __str__(self) -> str:
        return f"{self.razao_social} ({self.cnpj})"


class UsuarioCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente_profile', null=True, blank=True)
    nome_completo = models.CharField(max_length=200)
    telefone = models.CharField(max_length=30, blank=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    empresa_associada = models.ForeignKey(Empresa, on_delete=models.SET_NULL, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self) -> str:
        return f"{self.nome_completo} ({self.user.username})"
