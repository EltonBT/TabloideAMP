
import pandas as pd

# Dados dos itens do mercado
dados = [
    ["001", "Arroz Tipo 1 5kg", 23.90, "Arroz branco tipo 1, ideal para o dia a dia."],
    ["002", "Feijão Carioca 1kg", 8.50, "Feijão carioca selecionado, grãos de alta qualidade."],
    ["003", "Macarrão Espaguete 500g", 4.30, "Macarrão de sêmola enriquecido com ferro e ácido fólico."],
    ["004", "Açúcar Refinado 1kg", 3.20, "Açúcar refinado ideal para doces e receitas em geral."],
    ["005", "Café Torrado e Moído 500g", 12.90, "Café tradicional, sabor intenso e encorpado."],
    ["006", "Óleo de Soja 900ml", 6.70, "Óleo de soja refinado, ideal para frituras e receitas."],
    ["007", "Leite Integral 1L", 4.80, "Leite de vaca integral, fonte de cálcio e vitaminas."],
    ["008", "Margarina 500g", 6.20, "Margarina cremosa com sal, perfeita para pães e receitas."],
    ["009", "Papel Higiênico 12un", 18.90, "Rolo de papel higiênico folha dupla, maciez garantida."],
    ["010", "Detergente Líquido 500ml", 2.40, "Detergente para louças com alto poder desengordurante."],
    ["011", "Desinfetante 1L", 5.30, "Desinfetante com fragrância de pinho, elimina 99,9% dos germes."],
    ["012", "Shampoo 350ml", 10.90, "Shampoo para uso diário com fragrância suave."],
    ["013", "Amaciante de Roupas 2L", 12.50, "Deixa as roupas macias e perfumadas por mais tempo."],
    ["014", "Farinha de Trigo 1kg", 4.10, "Farinha branca enriquecida com ferro e ácido fólico."],
    ["015", "Frango Congelado 1kg", 10.90, "Frango inteiro congelado, ideal para assar ou cozinhar."],
    ["016", "Carne Moída Bovina 1kg", 24.90, "Carne moída de primeira, ideal para receitas diversas."],
    ["017", "Sabão em Pó 1kg", 9.80, "Remove manchas difíceis, ideal para roupas brancas e coloridas."],
    ["018", "Refrigerante Cola 2L", 7.20, "Bebida gaseificada sabor cola, ideal para festas."],
    ["019", "Biscoito Recheado 130g", 2.90, "Biscoito crocante com recheio sabor chocolate."],
    ["020", "Cereal Matinal 250g", 8.90, "Cereal matinal com vitaminas, ideal para café da manhã."]
]

# Criando o DataFrame
df = pd.DataFrame(dados, columns=["código", "nome", "preço", "descrição"])

# Salvando como arquivo CSV
df.to_csv("itens_supermercado.csv", index=False)
