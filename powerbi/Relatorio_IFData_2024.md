# Relatório Power BI — IFData 2024

## Situação
A base tratada está no CSV do modelo e em SQLite. O relatório `.pbix` foi criado no Power BI Desktop e tem quatro páginas: Visão geral, Rentabilidade, Crédito e Metodologia. As páginas analíticas incluem filtros de DataBase, TipoControle, SegmentoTCB e UF. O arquivo está em `outputs/rojeto_IFData_2024.pbix`.

Os cartões e páginas foram montados no aplicativo, com paleta coordenada nas páginas Rentabilidade e Crédito. As medidas Carteira/ativo e Lucro/PL final estão formatadas como percentuais. A conferência numérica independente está documentada abaixo. Alguns cartões ainda exibem a unidade automática `Mil` e o ativo está com três casas decimais; revisar a formatação numérica antes das capturas finais. Consulte o [README do projeto](../README.md) e a [página de apresentação do portfólio](../outputs/portfolio_IFData_2024.html).

## Fonte e escopo
IFData/BCB, relatório Resumo, tipo de instituição individual, data-base 12/2024. A base enviada tem 1.585 instituições e valores monetários em R$ mil. O BCB informa que os resultados de dezembro acumulam o período de janeiro a dezembro, e que `NI` significa não informado. O relatório inclui apenas instituições autorizadas em operação normal e apresenta os dados informados pelas instituições.

## Modelo a carregar
1. No Power BI Desktop, **Obter dados > Consulta em branco > Editor avançado** e cole `powerbi/Consulta_IFData.m`.
2. Renomeie a tabela importada para `FactIFData`.
3. Defina `CodigoInstituicao`, códigos de conglomerado, `TCB`, `TC_Codigo` e `TI_Codigo` como texto; `DataBase` como data; métricas monetárias e contagens como inteiro.
4. Importe as medidas de `powerbi/Medidas_IFData.dax` uma a uma. Formate as medidas `... (R$ bi)` como moeda em bilhões com 2 casas; as medidas `... (R$ mil)` como número inteiro; as medidas percentuais como percentual com 1 casa.
5. Configure fatiadores para `DataBase`, `SegmentoTCB`, `TCB`, `TipoControle`, `TI_Codigo`, `NomeConglomeradoPrudencial` e `UF`.

### Escopo dos filtros
- **Data:** há apenas uma data-base (`31/12/2024`), então o filtro terá uma opção. Não há análise de tendência até adicionar outros trimestres.
- **Grupo/tipo:** use nome/código do conglomerado prudencial, `TipoControle` e código `TI_Codigo`.
- **Segmento:** `SegmentoTCB` é um agrupamento analítico derivado do Tipo de Consolidado Bancário: Bancário (B1/B2/B4), Cooperativas (B3S/B3C) e Não bancário (N1/N2/N4). Não confundir com o segmento regulatório S1–S5; esse campo não existe neste CSV.

## Páginas e visuais

### 1. Visão geral
- Cartões: instituições analisadas; ativo total (R$ bi); carteira classificada (R$ bi); lucro líquido (R$ bi).
- Barras horizontais: 10 maiores instituições por ativo.
- Barras/colunas: ativo, crédito e lucro por `SegmentoTCB`.
- Filtros: data-base, segmento TCB, TCB, controle, tipo institucional, conglomerado prudencial e UF.

### 2. Rentabilidade
- Cartões: lucro líquido, patrimônio líquido, instituições com lucro e instituições com prejuízo.
- Barras horizontais: maiores e menores lucros por instituição; aplicar filtro Top 10 para a vista principal.
- Barras por segmento TCB e tipo de controle: lucro e medida `Lucro / PL final - proxy (%)`.
- Rótulo obrigatório: a razão Lucro/PL final é uma proxy descritiva, não ROE regulatório, pois usa PL de encerramento e não o patrimônio médio.

### 3. Crédito
- Cartões: carteira classificada (R$ bi) e carteira/ativo (%).
- Barras: instituições com maior carteira classificada.
- Barras por segmento TCB e tipo de controle: carteira e carteira/ativo.
- Limitação: o arquivo mede saldo/exposição de carteira classificada. Não contém inadimplência, atraso, provisões ou perda esperada; portanto, não permite concluir qualidade ou risco de crédito.

## Definições e unidades
- Ativo total, carteira classificada, passivo exigível, captações, patrimônio líquido e lucro líquido: valores do IFData em **R$ mil**. Para exibição em R$ bi, dividir o valor em R$ mil por 1.000.000.
- Carteira/ativo (%): carteira de crédito classificada ÷ ativo total. É proporção de saldo contábil, não taxa de inadimplência.
- Lucro/PL final - proxy (%): lucro líquido do exercício ÷ PL de encerramento. Não é ROE oficial; comparações por instituição devem ser interpretadas com cautela.
- Tipo de controle: TC 1 público, 2 privado nacional, 3 controle estrangeiro.
- TCB: categoria de consolidação bancária do IFData; `SegmentoTCB` agrega as categorias em três grupos didáticos definidos acima.
- Campos `NI` do CSV foram preservados como nulos na cópia tratada; nulo não significa zero.

## Conferência dos totais em SQL
A leitura Python/CSV e a consulta SQL reconciliaram exatamente os principais totais:

- 1.585 instituições; uma data-base.
- Ativo total: R$ 17.514.570.107 mil.
- Carteira classificada: R$ 6.467.481.843 mil.
- Patrimônio líquido: R$ 1.887.410.071 mil.
- Lucro líquido: R$ 154.080.056 mil.
- Instituições com lucro: 1.272; com prejuízo: 302; zero/não informado: 11.

Resumo por SegmentoTCB (SQL):
- Bancário: 174 instituições; ativo R$ 14.932.606.987 mil; carteira R$ 5.591.866.978 mil; lucro R$ 119.466.795 mil.
- Cooperativas: 782 instituições; ativo R$ 1.008.064.262 mil; carteira R$ 458.055.663 mil; lucro R$ 9.836.503 mil.
- Não bancário: 629 instituições; ativo R$ 1.573.898.858 mil; carteira R$ 417.559.202 mil; lucro R$ 24.776.758 mil.

Os valores acima usam apenas os registros individuais da cópia recebida, não os totais agregados no rodapé do CSV.

## Fontes
- [IFData no portal de dados abertos do BCB](https://dadosabertos.bcb.gov.br/dataset/ifdata---dados-selecionados-de-instituies-financeiras)
- [Metodologia IFData do BCB](https://www.bcb.gov.br/conteudo/dadosabertos/BCBDesig/IFData%20-%20Esclarecimentos%20e%20Metodologia.pdf)
- [Definições e nota sobre o exercício acumulado em dezembro — IFData](https://www3.bcb.gov.br/ifdata/index2024.html)
