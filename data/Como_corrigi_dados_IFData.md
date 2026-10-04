# Como corrigi o CSV do IFData

## Arquivos
- Original do usuário: `C:\Users\alerr\Downloads\dados.csv` (preservado, sem alterações)`n- Cópia bruta no projeto: `data/raw/dados_original.csv`
- Cópia de análise: `data/processed/dados_IFData_2024_limpo.csv`

## O que encontrei
- Arquivo separado por ponto e vírgula (`;`).
- Um relatório com data-base `12/2024`.
- 1.585 registros de instituições, seguidos por um bloco agregado com totais e percentuais por tipo (TCB).
- O cabeçalho repetia `Conglomerado Prudencial` e terminava com um ponto e vírgula, criando uma coluna sem nome.
- 42 células tinham o marcador `NI` (não informado).

## Ajustes feitos na cópia
1. Mantive somente as linhas de instituição cuja data-base é `12/2024`; o bloco agregado final continua preservado no original, mas não foi misturado à tabela de instituições.
2. Mantive as 19 colunas com dados e removi a coluna final vazia.
3. Renomeei os cabeçalhos para distinguir os campos: `Código da instituição`, `Nome do conglomerado prudencial`, `Código do conglomerado financeiro` e `Código do conglomerado prudencial`.
4. Converti `NI` em célula vazia. Isso significa não informado, não zero.
5. Salvei em UTF-8 com BOM e validei que a cópia tem 1.585 linhas de dados, 19 colunas únicas e apenas a data-base 12/2024.

## Como reproduzir no Excel
1. Abra uma nova planilha e selecione **Dados > Obter Dados > De Texto/CSV**.
2. Selecione `dados_IFData_2024_limpo.csv`.
3. Escolha delimitador **Ponto e vírgula** e codificação **UTF-8**.
4. Confirme a prévia: 19 colunas; a coluna `Data` deve conter `12/2024` em todas as linhas; campos sem informação ficam em branco.
5. Carregue como tabela. Mantenha o original separado para auditoria.

## Limite desta versão
O arquivo é uma fotografia de dezembro de 2024, não uma série temporal. Para analisar evolução, será necessário importar os mesmos relatórios para outras datas-base, mantendo o mesmo escopo de instituições/consolidação. Os valores monetários do IFData são apresentados em R$ mil; preserve essa unidade ao calcular e rotular gráficos.

