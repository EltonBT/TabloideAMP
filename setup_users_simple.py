import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tabloide_project.settings')
django.setup()

from django.contrib.auth.models import User
from relatorios.models import Empresa, UsuarioCliente

def create_user_if_not_exists(username, email, password, first_name="", last_name="", is_superuser=False, is_staff=False):
    """Cria usuário se não existir"""
    try:
        user = User.objects.get(username=username)
        print(f"AVISO: Usuario '{username}' ja existe")
        return user
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_staff=is_staff
        )
        print(f"OK: Usuario '{username}' criado com sucesso")
        return user

def create_empresa_if_not_exists(user, razao_social, cnpj, **kwargs):
    """Cria empresa se não existir"""
    try:
        empresa = Empresa.objects.get(user=user)
        print(f"AVISO: Empresa para usuario '{user.username}' ja existe")
        return empresa
    except Empresa.DoesNotExist:
        empresa = Empresa.objects.create(
            user=user,
            razao_social=razao_social,
            cnpj=cnpj,
            **kwargs
        )
        print(f"OK: Empresa '{razao_social}' criada para usuario '{user.username}'")
        return empresa

def create_cliente_if_not_exists(user, nome_completo, cpf, **kwargs):
    """Cria cliente se não existir"""
    try:
        cliente = UsuarioCliente.objects.get(user=user)
        print(f"AVISO: Cliente para usuario '{user.username}' ja existe")
        return cliente
    except UsuarioCliente.DoesNotExist:
        cliente = UsuarioCliente.objects.create(
            user=user,
            nome_completo=nome_completo,
            cpf=cpf,
            **kwargs
        )
        print(f"OK: Cliente '{nome_completo}' criado para usuario '{user.username}'")
        return cliente

print("=" * 60)
print("INICIANDO CRIACAO DE USUARIOS DE TESTE PARA TABLOIDEAMP")
print("=" * 60)

# 1. SUPERUSUÁRIO/ADMINISTRADOR
print("\n1. CRIANDO SUPERUSUARIO")
admin = create_user_if_not_exists(
    username="admin",
    email="admin@tabloideamp.com",
    password="admin123",
    first_name="Administrator",
    last_name="System",
    is_superuser=True,
    is_staff=True
)

# 2. USUÁRIOS EMPRESA
print("\n2. CRIANDO USUARIOS EMPRESA")

# Empresa 1: Supermercado
empresa1_user = create_user_if_not_exists(
    username="empresa1",
    email="contato@supermercadoexemplo.com",
    password="empresa123",
    first_name="Gestor",
    last_name="Supermercado"
)

empresa1 = create_empresa_if_not_exists(
    user=empresa1_user,
    razao_social="Supermercado Exemplo Ltda",
    nome_fantasia="Super Exemplo",
    cnpj="12.345.678/0001-90",
    ie="123456789",
    email="contato@supermercadoexemplo.com",
    telefone="(11) 99999-1234",
    endereco="Rua das Compras, 123",
    cidade="São Paulo",
    uf="SP",
    cep="01234-567"
)

# Empresa 2: Farmácia
empresa2_user = create_user_if_not_exists(
    username="farmacia",
    email="gerencia@farmaciasaude.com",
    password="farmacia123",
    first_name="Gerente",
    last_name="Farmacia"
)

empresa2 = create_empresa_if_not_exists(
    user=empresa2_user,
    razao_social="Farmacia Saude e Bem Estar Ltda",
    nome_fantasia="Farmacia Saude",
    cnpj="98.765.432/0001-10",
    ie="987654321",
    email="gerencia@farmaciasaude.com",
    telefone="(11) 88888-5678",
    endereco="Av. da Saude, 456",
    cidade="São Paulo",
    uf="SP",
    cep="04567-890"
)

# Empresa 3: Loja de Roupas
empresa3_user = create_user_if_not_exists(
    username="modafashion",
    email="vendas@modafashion.com",
    password="moda123",
    first_name="Estilista",
    last_name="Moda"
)

empresa3 = create_empresa_if_not_exists(
    user=empresa3_user,
    razao_social="Moda Fashion Confeccoes Ltda",
    nome_fantasia="Moda Fashion",
    cnpj="11.222.333/0001-44",
    ie="112233445",
    email="vendas@modafashion.com",
    telefone="(11) 77777-9012",
    endereco="Rua da Moda, 789",
    cidade="São Paulo",
    uf="SP",
    cep="01987-654"
)

# 3. USUÁRIOS CLIENTE
print("\n3. CRIANDO USUARIOS CLIENTE")

# Cliente 1
cliente1_user = create_user_if_not_exists(
    username="cliente1",
    email="joao.silva@email.com",
    password="cliente123",
    first_name="João",
    last_name="Silva"
)

cliente1 = create_cliente_if_not_exists(
    user=cliente1_user,
    nome_completo="João Silva Santos",
    cpf="123.456.789-00",
    email="joao.silva@email.com",
    telefone="(11) 99999-0001"
)

# Cliente 2
cliente2_user = create_user_if_not_exists(
    username="maria.cliente",
    email="maria.oliveira@email.com",
    password="cliente123",
    first_name="Maria",
    last_name="Oliveira"
)

cliente2 = create_cliente_if_not_exists(
    user=cliente2_user,
    nome_completo="Maria Oliveira Costa",
    cpf="987.654.321-00",
    email="maria.oliveira@email.com",
    telefone="(11) 88888-0002"
)

# Cliente 3
cliente3_user = create_user_if_not_exists(
    username="pedrocarlos",
    email="pedro.carlos@email.com",
    password="cliente123",
    first_name="Pedro",
    last_name="Carlos"
)

cliente3 = create_cliente_if_not_exists(
    user=cliente3_user,
    nome_completo="Pedro Carlos Ferreira",
    cpf="456.789.123-00",
    email="pedro.carlos@email.com",
    telefone="(11) 77777-0003"
)

# 4. USUÁRIO DE TESTE GERAL
print("\n4. CRIANDO USUARIO DE TESTE GERAL")
teste_user = create_user_if_not_exists(
    username="teste",
    email="teste@tabloideamp.com",
    password="teste123",
    first_name="Usuario",
    last_name="Teste",
    is_staff=True
)

print("\n" + "=" * 60)
print("CRIACAO DE USUARIOS CONCLUIDA COM SUCESSO!")
print("=" * 60)

print("\nRESUMO DOS USUARIOS CRIADOS:")
print("\nADMINISTRADOR:")
print("   Username: admin")
print("   Password: admin123")
print("   Email: admin@tabloideamp.com")
print("   Acesso: Total (Django Admin + Sistema)")

print("\nEMPRESAS:")
print("   1. Username: empresa1     | Password: empresa123 | Supermercado Exemplo")
print("   2. Username: farmacia     | Password: farmacia123 | Farmacia Saude")
print("   3. Username: modafashion  | Password: moda123     | Moda Fashion")

print("\nCLIENTES:")
print("   1. Username: cliente1     | Password: cliente123 | João Silva Santos")
print("   2. Username: maria.cliente| Password: cliente123 | Maria Oliveira Costa")
print("   3. Username: pedrocarlos  | Password: cliente123 | Pedro Carlos Ferreira")

print("\nTESTE:")
print("   Username: teste")
print("   Password: teste123")
print("   Email: teste@tabloideamp.com")

print("\nURLS DE ACESSO:")
print("   Sistema: http://localhost:8000/")
print("   Admin: http://localhost:8000/admin/")
print("   Escolher Area: http://localhost:8000/escolher-area/")

print("\nINSTRUCOES:")
print("   1. Use 'admin' para acesso total ao sistema")
print("   2. Use contas 'empresa*' para testar funcionalidades empresariais")
print("   3. Use contas 'cliente*' para testar area do cliente")
print("   4. Todas as senhas seguem o padrao: [tipo]123")

print("\nScript executado com sucesso!")