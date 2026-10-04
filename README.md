# Sistema Financeiro Brasileiro — análise do IFData/BCB 2024

Análise exploratória das instituições financeiras brasileiras a partir do IFData do Banco Central. O projeto percorre preparação em Excel/Python, estruturação e conferência em SQL e apresentação interativa no Power BI.

> **Escopo:** fotografia da data-base de 31/12/2024, com 1.585 instituições individuais. Este estudo não é uma série temporal.

## Pergunta de análise

Como se distribuem ativos, crédito e resultado entre instituições bancárias, cooperativas e instituições não bancárias? Quais são as diferenças descritivas entre os grupos e como os saldos de crédito se comparam aos ativos?

## Principais números

| Indicador | Resultado |
|---|---:|
| Instituições | 1.585 |
| Ativo total | R$ 17.514,57 bilhões |
| Carteira de crédito classificada | R$ 6.467,48 bilhões |
| Patrimônio líquido | R$ 1.887,41 bilhões |
| Lucro líquido | R$ 154,08 bilhões |
| Instituições com lucro / prejuízo | 1.272 / 302 |

O segmento bancário reúne 85,3% dos ativos, 86,5% da carteira classificada e 77,5% do lucro líquido. As cooperativas representam 49,3% das instituições, mas 5,8% dos ativos e 7,1% da carteira. O saldo de carteira equivale a 36,9% dos ativos na base total. São comparações descritivas deste recorte, não explicações causais nem medidas de risco.

## Ferramentas e fluxo

1. **Excel:** inspeção do CSV, cabeçalhos, delimitador, unidades e conferência pontual dos dados tratados.
2. **Python:** limpeza do arquivo, conversão dos números brasileiros para inteiros em R$ mil e criação do modelo analítico.
3. **SQL / SQLite:** agregações por segmento e instituição e reconciliação dos indicadores principais com Python.
4. **Power BI Desktop:** relatório interativo com páginas de visão geral, rentabilidade, crédito e metodologia.

## Resultado no Power BI

O relatório inclui filtros por data-base, tipo de controle, segmento TCB e UF. Como a base contém somente 31/12/2024, o filtro de data tem uma opção. Medidas principais e totais foram comparadas com as consultas SQLite.

**Arquivo:** [abrir o relatório Power BI](outputs/Projeto_IFData_2024.pbix)

**Página de apresentação do portfólio:** [abrir o estudo IFData 2024](outputs/portfolio_IFData_2024.html)

**Estado visual:** apliquei uma paleta coordenada aos cartões das páginas Rentabilidade e Crédito, aumentei os títulos dos gráficos e dei ao gráfico principal o título “Ativo total por segmento (R$ bi)”. As medidas de carteira/ativo e lucro/PL aparecem como percentuais (36,93% e 8,16%). A página HTML de portfólio apresenta os totais certificados. No `.pbix`, a unidade automática ainda aparece como `Mil` em alguns cartões e ativo está com três casas decimais; revisar a formatação numérica dos cartões de Visão geral, Rentabilidade e Crédito antes de capturar as telas finais.

## Preparação e modelagem

- O CSV original usa `;` como delimitador e números no padrão brasileiro.
- O cabeçalho tinha uma coluna final vazia e nomes de conglomerado repetidos; o conjunto tratado mantém as 19 colunas informativas com nomes distintos.
- Foram mantidas as linhas individuais de instituição para a data-base 12/2024; linhas de totalização do arquivo foram excluídas da tabela analítica.
- `NI` foi preservado como ausência (nulo), nunca convertido em zero.
- As medidas monetárias de origem estão em **R$ mil**. Para apresentar em **R$ bilhões**, o valor em R$ mil é dividido por 1.000.000.
- `SegmentoTCB` é uma classificação analítica derivada do campo TCB: Bancário (B1/B2/B4), Cooperativas (B3S/B3C) e Não bancário (N1/N2/N4). Não equivale à segmentação regulatória S1–S5.

## Indicadores e limites de interpretação

- **Carteira / ativo:** carteira de crédito classificada dividida pelo ativo total; representa participação dos saldos, não inadimplência.
- **Lucro / PL final — proxy:** lucro líquido dividido pelo patrimônio líquido de encerramento. Não é ROE regulatório, pois não usa o patrimônio médio e não reproduz a metodologia oficial de rentabilidade.
- O arquivo analisado não contém atrasos, inadimplência, provisões ou perdas esperadas. Portanto, não permite avaliar qualidade ou risco de crédito.
- Dezembro contém o resultado acumulado do exercício para medidas de fluxo, como lucro. Comparações com saldos patrimoniais devem respeitar essa diferença.
- A base representa instituições em operação normal segundo a cobertura do IFData. Não usar este recorte isolado para inferir trajetórias históricas de entidades encerradas.
- A estrutura contábil mudou em 2025; comparar períodos posteriores exige tratamento metodológico adicional.

## Conferência dos resultados

Os totais de Python/CSV e SQLite coincidem exatamente:

| Campo | Total em R$ mil | Equivalente em R$ bilhões |
|---|---:|---:|
| Ativo total | 17.514.570.107 | 17.514,57 |
| Carteira classificada | 6.467.481.843 | 6.467,48 |
| Patrimônio líquido | 1.887.410.071 | 1.887,41 |
| Lucro líquido | 154.080.056 | 154,08 |

Na classificação do resultado líquido há 1.272 instituições com lucro, 302 com prejuízo e 11 com resultado zero ou não informado.

## Estrutura do projeto

```text
data/
  raw/dados_original.csv
  processed/dados_IFData_2024_limpo.csv
  processed/ifdata_2024_modelo_powerbi.csv
  processed/ifdata_2024.sqlite
work/
  limpar_ifdata.py
  build_ifdata_model.py
sql/ifdata_2024_validacao.sql
powerbi/
  Consulta_IFData.m
  Medidas_IFData.dax
  Relatorio_IFData_2024.md
outputs/
  analise.ipynb
  portfolio_IFData_2024.html
  Projeto_IFData_2024.pbix
```

## Como reproduzir

Na pasta do projeto, com Python instalado:

```powershell
python work/limpar_ifdata.py
python work/build_ifdata_model.py
```

Para conferir no Excel, abra `data/processed/dados_IFData_2024_limpo.csv` como texto/CSV com delimitador ponto e vírgula e codificação UTF-8. Para a análise SQL, use o banco `data/processed/ifdata_2024.sqlite` e o arquivo `sql/ifdata_2024_validacao.sql`. Para abrir o dashboard, use o `.pbix` indicado acima. Após clonar o repositório, ajuste `ProjectFolder` no início de `powerbi/Consulta_IFData.m` para o caminho local da pasta do projeto e atualize a consulta no Power Query.

## Fontes

- [IFData — Banco Central do Brasil](https://www3.bcb.gov.br/ifdata/index2024.html?lang=1)
- [Conjunto IFData no Portal de Dados Abertos do BCB](https://dadosabertos.bcb.gov.br/dataset/ifdata---dados-selecionados-de-instituies-financeiras)
- [Metodologia e esclarecimentos do IFData](https://www.bcb.gov.br/estabilidadefinanceira/ifdata)

## Próximo passo

Finalizar a formatação numérica dos cartões no Power BI e capturar as quatro páginas do relatório. O README e a página HTML já resumem a análise; depois da revisão visual, podem ser publicados junto dos arquivos de apoio.
