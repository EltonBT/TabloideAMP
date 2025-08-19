from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from .forms import (
    ImportacaoTabelaForm,
    ItemTabloideForm,
    ProdutoForm,
    TemplateTabloideForm,
    EmpresaForm,
)
from .models import ItemTabloide, Produto, TemplateTabloide, Empresa


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "page_title": "Relatórios",
    }
    return render(request, "relatorios/home.html", context)


def signup(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("relatorios:home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# Produtos CRUD
class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    paginate_by = 20
    template_name = "relatorios/produtos/list.html"


class ProdutoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "relatorios.add_produto"
    model = Produto
    form_class = ProdutoForm
    template_name = "relatorios/produtos/form.html"
    success_url = reverse_lazy("relatorios:produto_list")


class ProdutoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "relatorios.change_produto"
    model = Produto
    form_class = ProdutoForm
    template_name = "relatorios/produtos/form.html"
    success_url = reverse_lazy("relatorios:produto_list")


class ProdutoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "relatorios.delete_produto"
    model = Produto
    template_name = "relatorios/produtos/confirm_delete.html"
    success_url = reverse_lazy("relatorios:produto_list")


# Empresas CRUD
class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    paginate_by = 20
    template_name = "relatorios/empresas/list.html"


class EmpresaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "relatorios.add_empresa"
    model = Empresa
    form_class = EmpresaForm
    template_name = "relatorios/empresas/form.html"
    success_url = reverse_lazy("relatorios:empresa_list")


class EmpresaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "relatorios.change_empresa"
    model = Empresa
    form_class = EmpresaForm
    template_name = "relatorios/empresas/form.html"
    success_url = reverse_lazy("relatorios:empresa_list")


class EmpresaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "relatorios.delete_empresa"
    model = Empresa
    template_name = "relatorios/empresas/confirm_delete.html"
    success_url = reverse_lazy("relatorios:empresa_list")


# Importação de tabela de preços
@login_required
@permission_required("relatorios.add_tabelaprecoimportacao", raise_exception=True)
def importar_tabela_precos(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ImportacaoTabelaForm(request.POST, request.FILES)
        if form.is_valid():
            importacao = form.save()
            # Processa CSV/XLSX: pressupõe colunas: codigo, nome, preco, codigo_barras, descricao
            try:
                import pandas as pd  # type: ignore

                caminho = importacao.arquivo.path
                if caminho.lower().endswith(".csv"):
                    df = pd.read_csv(caminho, dtype=str)
                else:
                    df = pd.read_excel(caminho, dtype=str)
                # Normaliza colunas
                colmap = {c.lower().strip(): c for c in df.columns}

                def get(col):
                    for k in [col, col.replace("ç", "c"), col.replace("á", "a")]:
                        if k in colmap:
                            return colmap[k]
                    return None

                col_codigo = get("codigo") or get("código")
                col_nome = get("nome")
                col_preco = get("preco") or get("preço")
                col_barras = (
                    get("codigo_barras")
                    or get("código de barras")
                    or get("codigo de barras")
                )
                col_desc = get("descricao") or get("descrição")
                for _, row in df.iterrows():
                    codigo = str(row.get(col_codigo, "")).strip() if col_codigo else ""
                    if not codigo:
                        continue
                    produto, _ = Produto.objects.get_or_create(codigo=codigo)
                    if col_nome:
                        produto.nome = (
                            str(row.get(col_nome, produto.nome or "")).strip()
                            or produto.nome
                        )
                    if col_desc:
                        produto.descricao = (
                            str(row.get(col_desc, produto.descricao or "")).strip()
                            or produto.descricao
                        )
                    if col_barras:
                        cb = str(row.get(col_barras, "")).strip()
                        if cb:
                            produto.codigo_barras = cb
                    if col_preco:
                        try:
                            preco_str = (
                                str(row.get(col_preco, "")).replace(",", ".").strip()
                            )
                            produto.preco = float(preco_str or 0)
                        except Exception:
                            pass
                    produto.save()
                importacao.processado = True
            except Exception:
                importacao.processado = False
            importacao.save(update_fields=["processado"])
            return redirect("relatorios:produto_list")
    else:
        form = ImportacaoTabelaForm()
    return render(request, "relatorios/importacao/form.html", {"form": form})


# Templates de tabloide
class TemplateTabloideListView(LoginRequiredMixin, ListView):
    model = TemplateTabloide
    template_name = "relatorios/tabloide/template_list.html"


class TemplateTabloideCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    permission_required = "relatorios.add_templatetabloide"
    model = TemplateTabloide
    form_class = TemplateTabloideForm
    template_name = "relatorios/tabloide/template_form.html"
    success_url = reverse_lazy("relatorios:template_list")


class TemplateTabloideUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    permission_required = "relatorios.change_templatetabloide"
    model = TemplateTabloide
    form_class = TemplateTabloideForm
    template_name = "relatorios/tabloide/template_form.html"
    success_url = reverse_lazy("relatorios:template_list")


@login_required
def gerenciar_itens_tabloide(request: HttpRequest, pk: int) -> HttpResponse:
    template = get_object_or_404(TemplateTabloide, pk=pk)
    if request.method == "POST":
        if not request.user.has_perm("relatorios.change_templatetabloide"):
            return redirect("login")
        form = ItemTabloideForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("relatorios:template_items", pk=template.pk)
    else:
        form = ItemTabloideForm(initial={"template": template})
    itens = template.itens.select_related("produto").all()
    return render(
        request,
        "relatorios/tabloide/itens.html",
        {"template": template, "form": form, "itens": itens},
    )


@login_required
@permission_required("relatorios.change_templatetabloide", raise_exception=True)
def remover_item_tabloide(
    request: HttpRequest, template_pk: int, item_pk: int
) -> HttpResponse:
    template = get_object_or_404(TemplateTabloide, pk=template_pk)
    item = get_object_or_404(ItemTabloide, pk=item_pk, template=template)
    if request.method == "POST":
        item.delete()
        return redirect("relatorios:template_items", pk=template.pk)
    return render(
        request,
        "relatorios/tabloide/confirm_remove_item.html",
        {"template": template, "item": item},
    )


@login_required
def perfil(request: HttpRequest) -> HttpResponse:
    user = request.user
    grupos = list(user.groups.values_list("name", flat=True))
    context = {
        "page_title": "Meu Perfil",
        "user_obj": user,
        "grupos": grupos,
    }
    return render(request, "relatorios/perfil.html", context)


def gerar_pdf_tabloide(request: HttpRequest) -> HttpResponse:
    """Gera PDF em tabloide (11x17) com layout baseado em TemplateTabloide e seus itens."""
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=relatorio_tabloide.pdf"
    response["X-Frame-Options"] = "SAMEORIGIN"

    pagina_largura = 11 * inch
    pagina_altura = 17 * inch
    pdf = canvas.Canvas(response, pagesize=(pagina_largura, pagina_altura))

    margem = 0.75 * inch
    pdf.setTitle("Tabloide")

    template_id = request.GET.get("template")
    template: TemplateTabloide | None = None
    if template_id:
        try:
            template = TemplateTabloide.objects.get(pk=int(template_id))
        except Exception:
            template = None
    if template is None:
        template = TemplateTabloide.objects.first()

    if template:
        colunas = max(1, template.colunas)
        linhas = max(1, template.linhas)
        largura_util = pagina_largura - 2 * margem
        altura_util = pagina_altura - 2 * margem
        largura_celula = largura_util / colunas
        altura_celula = altura_util / linhas

        itens = list(template.itens.select_related("produto"))
        # Desenha imagem de fundo caso exista
        try:
            if template.background_imagem and template.background_imagem.path:
                pdf.drawImage(
                    template.background_imagem.path,
                    0,
                    0,
                    width=pagina_largura,
                    height=pagina_altura,
                    preserveAspectRatio=True,
                    mask="auto",
                )
        except Exception:
            pass
        # Desenha fundo por linha
        try:
            from reportlab.lib.colors import HexColor

            bg_color = HexColor(template.cor_fundo_row)
        except Exception:
            bg_color = colors.whitesmoke
        y = pagina_altura - margem
        for l in range(linhas):
            y -= altura_celula
            pdf.setFillColor(bg_color)
            pdf.rect(margem, y, largura_util, altura_celula, fill=1, stroke=0)
        # Conteúdo
        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica-Bold", 12)
        idx = 0
        for r in range(linhas):
            for c in range(colunas):
                if idx >= len(itens):
                    break
                item = itens[idx]
                produto = item.produto
                x0 = margem + c * largura_celula
                y0 = pagina_altura - margem - (r + 1) * altura_celula
                padding = 8
                pdf.drawString(
                    x0 + padding, y0 + altura_celula - padding - 14, produto.nome[:40]
                )
                pdf.setFont("Helvetica", 10)
                pdf.drawString(
                    x0 + padding,
                    y0 + altura_celula - padding - 32,
                    f"R$ {produto.preco:,.2f}",
                )
                idx += 1
    else:
        # Exemplo genérico de tabloide 3x4 com itens fictícios
        colunas = 3
        linhas = 4
        largura_util = pagina_largura - 2 * margem
        altura_util = pagina_altura - 2 * margem
        largura_celula = largura_util / colunas
        altura_celula = altura_util / linhas

        # Título
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(
            margem,
            pagina_altura - margem,
            "Exemplo - Tabloide (sem template cadastrado)",
        )

        # Fundo por linha
        from reportlab.lib.colors import HexColor

        bg_color = HexColor("#F2F4F7")
        y = pagina_altura - margem - 24
        for _ in range(linhas):
            y -= altura_celula
            pdf.setFillColor(bg_color)
            pdf.rect(margem, y, largura_util, altura_celula, fill=1, stroke=0)

        # Itens fictícios
        pdf.setFillColor(colors.black)
        nomes = [
            "Produto A",
            "Produto B",
            "Produto C",
            "Produto D",
            "Produto E",
            "Produto F",
            "Produto G",
            "Produto H",
            "Produto I",
            "Produto J",
            "Produto K",
            "Produto L",
        ]
        precos = [
            19.90,
            29.90,
            39.90,
            49.90,
            59.90,
            69.90,
            79.90,
            89.90,
            99.90,
            109.90,
            119.90,
            129.90,
        ]
        idx = 0
        for r in range(linhas):
            for c in range(colunas):
                x0 = margem + c * largura_celula
                y0 = pagina_altura - margem - 24 - (r + 1) * altura_celula
                padding = 8
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(
                    x0 + padding, y0 + altura_celula - padding - 14, nomes[idx]
                )
                pdf.setFont("Helvetica", 10)
                pdf.drawString(
                    x0 + padding,
                    y0 + altura_celula - padding - 32,
                    f"R$ {precos[idx]:,.2f}",
                )
                idx += 1

    pdf.showPage()
    pdf.save()
    return response


def gerar_jpeg_tabloide(request: HttpRequest) -> HttpResponse:
    """Exporta uma imagem JPEG simples do tabloide usando Pillow."""
    from io import BytesIO
    from PIL import Image, ImageDraw, ImageFont

    largura_px, altura_px = (3300, 5100)  # 11x17 @ 300 DPI
    img = Image.new("RGB", (largura_px, altura_px), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    template = TemplateTabloide.objects.first()
    colunas = template.colunas if template else 3
    linhas = template.linhas if template else 4

    margem = 100
    largura_util = largura_px - 2 * margem
    altura_util = altura_px - 2 * margem
    largura_cel = largura_util // colunas
    altura_cel = altura_util // linhas

    # Se houver imagem de fundo, aplica antes
    try:
        if template and template.background_imagem and template.background_imagem.path:
            from PIL import Image as PILImage

            bg_img = PILImage.open(template.background_imagem.path).convert("RGB")
            bg_img = bg_img.resize((largura_px, altura_px))
            img.paste(bg_img, (0, 0))
    except Exception:
        pass

    # Fundo das linhas
    try:
        hex_color = template.cor_fundo_row.lstrip("#") if template else "EEEEEE"
        bg = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    except Exception:
        bg = (238, 238, 238)
    for r in range(linhas):
        y0 = margem + r * altura_cel
        draw.rectangle([margem, y0, margem + largura_util, y0 + altura_cel], fill=bg)

    # Conteúdo
    itens = list(template.itens.select_related("produto")) if template else []
    idx = 0
    for r in range(linhas):
        for c in range(colunas):
            if idx >= len(itens):
                break
            produto = itens[idx].produto
            x0 = margem + c * largura_cel
            y0 = margem + r * altura_cel
            draw.text((x0 + 16, y0 + 16), produto.nome[:40], fill=(0, 0, 0))
            draw.text((x0 + 16, y0 + 48), f"R$ {produto.preco:,.2f}", fill=(20, 20, 20))
            idx += 1

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=90)
    buffer.seek(0)
    return FileResponse(buffer, content_type="image/jpeg")


def gerar_pdf_exemplo(request: HttpRequest) -> HttpResponse:
    """Gera um PDF simples de Pedido (A4) com itens de exemplo para exibir na home."""
    from datetime import date

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=pedido_exemplo.pdf"
    response["X-Frame-Options"] = "SAMEORIGIN"

    pagina_largura, pagina_altura = A4
    pdf = canvas.Canvas(response, pagesize=A4)

    margem = 36  # ~0.5in
    x0 = margem
    y_top = pagina_altura - margem

    # Cabeçalho
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x0, y_top, "TabloideMP")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        x0, y_top - 16, "CNPJ: 00.000.000/0000-00 • contato@tabloidemp.local"
    )

    # Título e metadados do pedido
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawRightString(pagina_largura - margem, y_top, "Pedido de Venda")
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(
        pagina_largura - margem,
        y_top - 16,
        f"Nº PED-0001 • {date.today().strftime('%d/%m/%Y')}",
    )

    # Dados do cliente
    y = y_top - 48
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x0, y, "Cliente")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(x0, y - 14, "Nome: Cliente Exemplo LTDA")
    pdf.drawString(x0, y - 28, "Documento: 123.456.789-00")
    pdf.drawString(x0, y - 42, "Endereço: Rua Exemplo, 123 - Centro - Cidade/UF")
    y -= 66

    # Tabela de itens (larguras fixas e alinhamento consistente)
    colunas = [
        ("Cód.", 60, "left"),
        ("Descrição", 260, "left"),
        ("Qtde", 60, "right"),
        ("Preço", 80, "right"),
        ("Subtotal", 90, "right"),
    ]
    padding = 6
    row_height = 18
    # Calcula inícios e fins de coluna
    col_starts = [x0]
    for _, w, _ in colunas:
        col_starts.append(col_starts[-1] + w)
    col_ends = col_starts[1:]
    col_starts = col_starts[:-1]

    # Cabeçalho da tabela
    pdf.setFont("Helvetica-Bold", 10)
    for i, (titulo, largura, align) in enumerate(colunas):
        start = col_starts[i]
        end = col_ends[i]
        if align == "right":
            pdf.drawRightString(end - padding, y, titulo)
        else:
            pdf.drawString(start + padding, y, titulo)
    y -= 6
    pdf.line(x0, y, col_ends[-1], y)
    y -= 12

    itens = [
        ("P001", "Produto A", 2, 19.90),
        ("P002", "Produto B", 1, 49.90),
        ("P003", "Produto C", 3, 9.90),
        ("P004", "Produto D", 1, 129.90),
        ("P005", "Produto E", 6, 129.90),
        ("P006", "Produto F", 3, 129.90),
        ("P007", "Produto G", 1, 129.90),
        ("P008", "Produto H", 4, 129.90),
        ("P009", "Produto I", 1, 129.90),
        ("P010", "Produto J", 3, 129.90),
        ("P011", "Produto K", 1, 129.90),
    ]
    total = 0.0
    pdf.setFont("Helvetica", 10)

    def fit_text(
        text: str, max_width: float, font_name: str = "Helvetica", font_size: int = 10
    ) -> str:
        # Trunca com … se ultrapassar a largura
        if pdf.stringWidth(text, font_name, font_size) <= max_width:
            return text
        ellipsis = "…"
        while (
            text and pdf.stringWidth(text + ellipsis, font_name, font_size) > max_width
        ):
            text = text[:-1]
        return text + ellipsis if text else ellipsis

    for cod, desc, qtde, preco in itens:
        subtotal = qtde * preco
        total += subtotal
        # Coluna 0: código (left)
        start, end = col_starts[0], col_ends[0]
        pdf.drawString(start + padding, y, str(cod))
        # Coluna 1: descrição (left, ajusta largura)
        start, end = col_starts[1], col_ends[1]
        max_w = (end - start) - 2 * padding
        desc_fit = fit_text(str(desc), max_w)
        pdf.drawString(start + padding, y, desc_fit)
        # Coluna 2: qtde (right)
        start, end = col_starts[2], col_ends[2]
        pdf.drawRightString(end - padding, y, f"{qtde}")
        # Coluna 3: preço (right)
        start, end = col_starts[3], col_ends[3]
        pdf.drawRightString(end - padding, y, f"R$ {preco:,.2f}")
        # Coluna 4: subtotal (right)
        start, end = col_starts[4], col_ends[4]
        pdf.drawRightString(end - padding, y, f"R$ {subtotal:,.2f}")
        # Linha separadora
        y -= row_height
        pdf.setStrokeColor(colors.lightgrey)
        # pdf.line(x0, y + 4, col_ends[-1], y + 4)
        pdf.setStrokeColor(colors.black)

    # Totais
    y -= 6
    pdf.line(x0, y, col_ends[-1], y)
    y -= 18
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(pagina_largura - margem - 140, y, "Total:")
    pdf.drawRightString(pagina_largura - margem, y, f"R$ {total:,.2f}")

    # Rodapé
    pdf.setFont("Helvetica", 9)
    pdf.drawString(
        x0, margem, "Observações: Este é um pedido de exemplo gerado automaticamente."
    )

    pdf.showPage()
    pdf.save()
    return response
