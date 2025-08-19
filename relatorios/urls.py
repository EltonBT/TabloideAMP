from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


app_name = "relatorios"


urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("perfil/", views.perfil, name="perfil"),
    # Empresas CRUD
    path("empresas/", views.EmpresaListView.as_view(), name="empresa_list"),
    path("empresas/novo/", views.EmpresaCreateView.as_view(), name="empresa_create"),
    path(
        "empresas/<int:pk>/editar/",
        views.EmpresaUpdateView.as_view(),
        name="empresa_update",
    ),
    path(
        "empresas/<int:pk>/excluir/",
        views.EmpresaDeleteView.as_view(),
        name="empresa_delete",
    ),
    # Produtos CRUD
    path("produtos/", views.ProdutoListView.as_view(), name="produto_list"),
    path("produtos/novo/", views.ProdutoCreateView.as_view(), name="produto_create"),
    path(
        "produtos/<int:pk>/editar/",
        views.ProdutoUpdateView.as_view(),
        name="produto_update",
    ),
    path(
        "produtos/<int:pk>/excluir/",
        views.ProdutoDeleteView.as_view(),
        name="produto_delete",
    ),
    # Importação
    path("importacao/", views.importar_tabela_precos, name="importacao"),
    # Tabloide
    path(
        "tabloide/templates/",
        views.TemplateTabloideListView.as_view(),
        name="template_list",
    ),
    path(
        "tabloide/templates/novo/",
        views.TemplateTabloideCreateView.as_view(),
        name="template_create",
    ),
    path(
        "tabloide/templates/<int:pk>/editar/",
        views.TemplateTabloideUpdateView.as_view(),
        name="template_update",
    ),
    path(
        "tabloide/templates/<int:pk>/itens/",
        views.gerenciar_itens_tabloide,
        name="template_items",
    ),
    path(
        "tabloide/templates/<int:template_pk>/itens/<int:item_pk>/remover/",
        views.remover_item_tabloide,
        name="template_item_remove",
    ),
    path("pdf/tabloide/", views.gerar_pdf_tabloide, name="pdf_tabloide"),
    path("jpeg/tabloide/", views.gerar_jpeg_tabloide, name="jpeg_tabloide"),
    path("pdf/exemplo/", views.gerar_pdf_exemplo, name="pdf_exemplo"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
