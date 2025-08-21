from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps
from .models import Empresa, UsuarioCliente


def empresa_required(view_func):
    """
    Decorator que requer que o usuário seja uma empresa logada
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('relatorios:empresa_login')
        
        # Permitir superusuário/admin acessar tudo
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        try:
            request.user.empresa_profile
            return view_func(request, *args, **kwargs)
        except Empresa.DoesNotExist:
            # Se é um usuário logado mas sem perfil empresa, redirecionar para escolha de área
            return redirect('relatorios:escolher_area')
    
    return _wrapped_view


def cliente_required(view_func):
    """
    Decorator que requer que o usuário seja um cliente logado
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('relatorios:cliente_login')
        
        # Permitir superusuário/admin acessar tudo
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        try:
            request.user.cliente_profile
            return view_func(request, *args, **kwargs)
        except UsuarioCliente.DoesNotExist:
            # Se é um usuário logado mas sem perfil cliente, redirecionar para escolha de área
            return redirect('relatorios:escolher_area')
    
    return _wrapped_view


class EmpresaRequiredMixin:
    """
    Mixin para class-based views que requer usuário empresa
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('relatorios:empresa_login')
        
        # Permitir superusuário/admin acessar tudo
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            request.user.empresa_profile
            return super().dispatch(request, *args, **kwargs)
        except Empresa.DoesNotExist:
            # Se é um usuário logado mas sem perfil empresa, redirecionar para escolha de área
            return redirect('relatorios:escolher_area')


class ClienteRequiredMixin:
    """
    Mixin para class-based views que requer usuário cliente
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('relatorios:cliente_login')
        
        # Permitir superusuário/admin acessar tudo
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            request.user.cliente_profile
            return super().dispatch(request, *args, **kwargs)
        except UsuarioCliente.DoesNotExist:
            # Se é um usuário logado mas sem perfil cliente, redirecionar para escolha de área
            return redirect('relatorios:escolher_area')