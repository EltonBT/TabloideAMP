import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tabloide_project.settings')
django.setup()

from django.contrib.auth.models import User
from relatorios.models import Empresa, UsuarioCliente

# Cores para output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def create_user_if_not_exists(username, email, password, first_name="", last_name="", is_superuser=False, is_staff=False):
    """Cria usuário se não existir"""
    try:
        user = User.objects.get(username=username)
        print(f"{Colors.YELLOW}⚠️  Usuário '{username}' já existe{Colors.END}")
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
        print(f"{Colors.GREEN}✅ Usuário '{username}' criado com sucesso{Colors.END}")
        return user

def create_empresa_if_not_exists(user, razao_social, cnpj, **kwargs):
    """Cria empresa se não existir"""
    try:
        empresa = Empresa.objects.get(user=user)
        print(f"{Colors.YELLOW}⚠️  Empresa para usuário '{user.username}' já existe{Colors.END}")
        return empresa
    except Empresa.DoesNotExist:
        empresa = Empresa.objects.create(
            user=user,
            razao_social=razao_social,
            cnpj=cnpj,
            **kwargs
        )
        print(f"{Colors.GREEN}✅ Empresa '{razao_social}' criada para usuário '{user.username}'{Colors.END}")
        return empresa

def create_cliente_if_not_exists(user, nome_completo, cpf, **kwargs):
    """Cria cliente se não existir"""
    try:
        cliente = UsuarioCliente.objects.get(user=user)
        print(f"{Colors.YELLOW}⚠️  Cliente para usuário '{user.username}' já existe{Colors.END}")
        return cliente
    except UsuarioCliente.DoesNotExist:
        cliente = UsuarioCliente.objects.create(
            user=user,
            nome_completo=nome_completo,
            cpf=cpf,
            **kwargs
        )
        print(f"{Colors.GREEN}✅ Cliente '{nome_completo}' criado para usuário '{user.username}'{Colors.END}")
        return cliente

print(f"{Colors.BOLD}{Colors.BLUE}🚀 Iniciando criação de usuários de teste para TabloideAMP{Colors.END}")
print("=" * 60)

# 1. SUPERUSUÁRIO/ADMINISTRADOR
print(f"\n{Colors.BOLD}👑 CRIANDO SUPERUSUÁRIO{Colors.END}")
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
print(f"\n{Colors.BOLD}🏢 CRIANDO USUÁRIOS EMPRESA{Colors.END}")

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
    last_name="Farmácia"
)

empresa2 = create_empresa_if_not_exists(
    user=empresa2_user,
    razao_social="Farmácia Saúde e Bem Estar Ltda",
    nome_fantasia="Farmácia Saúde",
    cnpj="98.765.432/0001-10",
    ie="987654321",
    email="gerencia@farmaciasaude.com",
    telefone="(11) 88888-5678",
    endereco="Av. da Saúde, 456",
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
    razao_social="Moda Fashion Confecções Ltda",
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
print(f"\n{Colors.BOLD}👤 CRIANDO USUÁRIOS CLIENTE{Colors.END}")

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
print(f"\n{Colors.BOLD}🧪 CRIANDO USUÁRIO DE TESTE{Colors.END}")
teste_user = create_user_if_not_exists(
    username="teste",
    email="teste@tabloideamp.com",
    password="teste123",
    first_name="Usuário",
    last_name="Teste",
    is_staff=True
)

print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 CRIAÇÃO DE USUÁRIOS CONCLUÍDA!{Colors.END}")
print("=" * 60)

print(f"\n{Colors.BOLD}📋 RESUMO DOS USUÁRIOS CRIADOS:{Colors.END}")
print(f"\n{Colors.BOLD}👑 ADMINISTRADOR:{Colors.END}")
print(f"   Username: admin")
print(f"   Password: admin123")
print(f"   Email: admin@tabloideamp.com")
print(f"   Acesso: Total (Django Admin + Sistema)")

print(f"\n{Colors.BOLD}🏢 EMPRESAS:{Colors.END}")
print(f"   1. Username: empresa1     | Password: empresa123 | Supermercado Exemplo")
print(f"   2. Username: farmacia     | Password: farmacia123 | Farmácia Saúde")
print(f"   3. Username: modafashion  | Password: moda123     | Moda Fashion")

print(f"\n{Colors.BOLD}👤 CLIENTES:{Colors.END}")
print(f"   1. Username: cliente1     | Password: cliente123 | João Silva Santos")
print(f"   2. Username: maria.cliente| Password: cliente123 | Maria Oliveira Costa")
print(f"   3. Username: pedrocarlos  | Password: cliente123 | Pedro Carlos Ferreira")

print(f"\n{Colors.BOLD}🧪 TESTE:{Colors.END}")
print(f"   Username: teste")
print(f"   Password: teste123")
print(f"   Email: teste@tabloideamp.com")

print(f"\n{Colors.BOLD}🌐 URLS DE ACESSO:{Colors.END}")
print(f"   Sistema: http://localhost:8000/")
print(f"   Admin: http://localhost:8000/admin/")
print(f"   Escolher Área: http://localhost:8000/escolher-area/")

print(f"\n{Colors.BOLD}💡 INSTRUÇÕES:{Colors.END}")
print(f"   1. Use 'admin' para acesso total ao sistema")
print(f"   2. Use contas 'empresa*' para testar funcionalidades empresariais")
print(f"   3. Use contas 'cliente*' para testar área do cliente")
print(f"   4. Todas as senhas seguem o padrão: [tipo]123")

print(f"\n{Colors.GREEN}✅ Script executado com sucesso!{Colors.END}")