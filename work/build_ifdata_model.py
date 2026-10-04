import csv, json, sqlite3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / 'data' / 'processed' / 'dados_IFData_2024_limpo.csv'
processed = root / 'data' / 'processed'
sql_dir = root / 'sql'
pbi_dir = root / 'powerbi'
sql_dir.mkdir(exist_ok=True)
pbi_dir.mkdir(exist_ok=True)

# Convert the BCB's pt-BR numeric text to integer values in R$ thousands.
def parse_num(value):
    value = (value or '').strip()
    if not value:
        return None
    return int(value.replace('.', '').replace(',', '.'))

with src.open(encoding='utf-8-sig', newline='') as f:
    original = list(csv.DictReader(f, delimiter=';'))

TCB_DESC = {
 'B1': 'Banco comercial/múltiplo com carteira comercial ou caixa econômica',
 'B2': 'Banco múltiplo sem carteira comercial, banco de câmbio ou investimento',
 'B3S': 'Cooperativa de crédito singular',
 'B3C': 'Central/confederação de cooperativas de crédito',
 'B4': 'Banco de desenvolvimento',
 'N1': 'Instituição não bancária de crédito',
 'N2': 'Instituição não bancária do mercado de capitais',
 'N4': 'Instituição de pagamento'
}
TCB_SEGMENT = {
 'B1': 'Bancário', 'B2': 'Bancário', 'B4': 'Bancário',
 'B3S': 'Cooperativas', 'B3C': 'Cooperativas',
 'N1': 'Não bancário', 'N2': 'Não bancário', 'N4': 'Não bancário'
}
TC_DESC = {'1': 'Público', '2': 'Privado nacional', '3': 'Controle estrangeiro'}

model_rows=[]
for r in original:
    tcb=(r['TCB'] or '').strip().upper()
    tc=(r['TC'] or '').strip()
    model_rows.append({
      'Instituicao': (r['Instituição'] or '').strip(),
      'CodigoInstituicao': (r['Código da instituição'] or '').strip(),
      'NomeConglomeradoPrudencial': (r['Nome do conglomerado prudencial'] or '').strip() or None,
      'CodigoConglomeradoFinanceiro': (r['Código do conglomerado financeiro'] or '').strip() or None,
      'CodigoConglomeradoPrudencial': (r['Código do conglomerado prudencial'] or '').strip() or None,
      'TCB': tcb,
      'DescricaoTCB': TCB_DESC.get(tcb, 'Não mapeado'),
      'SegmentoTCB': TCB_SEGMENT.get(tcb, 'Não mapeado'),
      'TC_Codigo': tc,
      'TipoControle': TC_DESC.get(tc, 'Não informado'),
      'TI_Codigo': (r['TI'] or '').strip(),
      'Cidade': (r['Cidade'] or '').strip(),
      'UF': (r['UF'] or '').strip(),
      'DataBase': '2024-12-31',
      'AtivoTotal_R_mil': parse_num(r['Ativo Total']),
      'CarteiraCreditoClassificada_R_mil': parse_num(r['Carteira de Crédito Classificada']),
      'PassivoExigivel_R_mil': parse_num(r['Passivo Circulante e Exigível a Longo Prazo e Resultados de Exercícios Futuros']),
      'Captacoes_R_mil': parse_num(r['Captações']),
      'PatrimonioLiquido_R_mil': parse_num(r['Patrimônio Líquido']),
      'LucroLiquido_R_mil': parse_num(r['Lucro Líquido']),
      'NumeroAgencias': parse_num(r['Número de Agências']),
      'NumeroPostosAtendimento': parse_num(r['Número de Postos de Atendimento'])
    })

model_csv=processed/'ifdata_2024_modelo_powerbi.csv'
with model_csv.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(model_rows[0]),delimiter=';',lineterminator='\n')
    w.writeheader(); w.writerows(model_rows)

sql_path=sql_dir/'ifdata_2024_validacao.sql'
db_path=processed/'ifdata_2024.sqlite'
sql_text='''-- IFData: base individual, data-base 31/12/2024. Valores em R$ mil.
-- SegmentoTCB é um agrupamento analítico construído a partir do TCB,
-- não equivale aos segmentos regulatórios S1-S5.
DROP VIEW IF EXISTS vw_kpis;
DROP VIEW IF EXISTS vw_segmentos;
DROP VIEW IF EXISTS vw_top_ativos;
DROP VIEW IF EXISTS vw_top_lucro;
CREATE VIEW vw_kpis AS
SELECT DataBase,
       COUNT(*) AS instituicoes,
       SUM(AtivoTotal_R_mil) AS ativo_total_R_mil,
       SUM(CarteiraCreditoClassificada_R_mil) AS carteira_credito_R_mil,
       SUM(PatrimonioLiquido_R_mil) AS patrimonio_liquido_R_mil,
       SUM(LucroLiquido_R_mil) AS lucro_liquido_R_mil,
       SUM(CASE WHEN LucroLiquido_R_mil > 0 THEN 1 ELSE 0 END) AS instituicoes_com_lucro,
       SUM(CASE WHEN LucroLiquido_R_mil < 0 THEN 1 ELSE 0 END) AS instituicoes_com_prejuizo,
       1.0 * SUM(CarteiraCreditoClassificada_R_mil) / NULLIF(SUM(AtivoTotal_R_mil),0) AS carteira_sobre_ativo,
       1.0 * SUM(LucroLiquido_R_mil) / NULLIF(SUM(PatrimonioLiquido_R_mil),0) AS lucro_sobre_PL_final_proxy
FROM instituicoes GROUP BY DataBase;
CREATE VIEW vw_segmentos AS
SELECT DataBase, SegmentoTCB,
       COUNT(*) AS instituicoes,
       SUM(AtivoTotal_R_mil) AS ativo_total_R_mil,
       SUM(CarteiraCreditoClassificada_R_mil) AS carteira_credito_R_mil,
       SUM(PatrimonioLiquido_R_mil) AS patrimonio_liquido_R_mil,
       SUM(LucroLiquido_R_mil) AS lucro_liquido_R_mil
FROM instituicoes GROUP BY DataBase, SegmentoTCB;
CREATE VIEW vw_top_ativos AS
SELECT Instituicao, SegmentoTCB, AtivoTotal_R_mil, CarteiraCreditoClassificada_R_mil,
       PatrimonioLiquido_R_mil, LucroLiquido_R_mil
FROM instituicoes ORDER BY AtivoTotal_R_mil DESC LIMIT 10;
CREATE VIEW vw_top_lucro AS
SELECT Instituicao, SegmentoTCB, AtivoTotal_R_mil, PatrimonioLiquido_R_mil, LucroLiquido_R_mil
FROM instituicoes ORDER BY LucroLiquido_R_mil DESC LIMIT 10;

-- Consulta detalhada por filtros: edite os valores abaixo ou remova as condições.
SELECT SegmentoTCB, TCB, TipoControle, TI_Codigo,
       COUNT(*) AS instituicoes,
       SUM(AtivoTotal_R_mil) AS ativo_total_R_mil,
       SUM(CarteiraCreditoClassificada_R_mil) AS carteira_credito_R_mil,
       SUM(LucroLiquido_R_mil) AS lucro_liquido_R_mil
FROM instituicoes
WHERE DataBase = '2024-12-31'
GROUP BY SegmentoTCB, TCB, TipoControle, TI_Codigo
ORDER BY ativo_total_R_mil DESC;
'''
sql_path.write_text(sql_text,encoding='utf-8')

schema='''CREATE TABLE instituicoes (
 Instituicao TEXT NOT NULL, CodigoInstituicao TEXT, NomeConglomeradoPrudencial TEXT,
 CodigoConglomeradoFinanceiro TEXT, CodigoConglomeradoPrudencial TEXT,
 TCB TEXT, DescricaoTCB TEXT, SegmentoTCB TEXT, TC_Codigo TEXT, TipoControle TEXT,
 TI_Codigo TEXT, Cidade TEXT, UF TEXT, DataBase TEXT NOT NULL,
 AtivoTotal_R_mil INTEGER, CarteiraCreditoClassificada_R_mil INTEGER,
 PassivoExigivel_R_mil INTEGER, Captacoes_R_mil INTEGER,
 PatrimonioLiquido_R_mil INTEGER, LucroLiquido_R_mil INTEGER,
 NumeroAgencias INTEGER, NumeroPostosAtendimento INTEGER
)'''
conn=sqlite3.connect(db_path)
cur=conn.cursor(); cur.execute('DROP TABLE IF EXISTS instituicoes'); cur.execute(schema)
cols=list(model_rows[0])
ins='INSERT INTO instituicoes ('+','.join(cols)+') VALUES ('+','.join('?' for _ in cols)+')'
cur.executemany(ins,[[r[c] for c in cols] for r in model_rows]); conn.commit()
cur.execute('CREATE INDEX IF NOT EXISTS ix_inst_segment ON instituicoes(SegmentoTCB,TCB,TipoControle,TI_Codigo)')
conn.executescript(sql_text)
conn.commit()
# Reconcile the headline metrics from source-import calculations with SQLite.
cur.execute('SELECT COUNT(*), SUM(AtivoTotal_R_mil), SUM(CarteiraCreditoClassificada_R_mil), SUM(PatrimonioLiquido_R_mil), SUM(LucroLiquido_R_mil), SUM(CASE WHEN LucroLiquido_R_mil>0 THEN 1 ELSE 0 END), SUM(CASE WHEN LucroLiquido_R_mil<0 THEN 1 ELSE 0 END) FROM instituicoes')
sql_metrics=cur.fetchone()
py_metrics=(len(model_rows),sum(r['AtivoTotal_R_mil'] or 0 for r in model_rows),sum(r['CarteiraCreditoClassificada_R_mil'] or 0 for r in model_rows),sum(r['PatrimonioLiquido_R_mil'] or 0 for r in model_rows),sum(r['LucroLiquido_R_mil'] or 0 for r in model_rows),sum(1 for r in model_rows if (r['LucroLiquido_R_mil'] or 0)>0),sum(1 for r in model_rows if (r['LucroLiquido_R_mil'] or 0)<0))
assert sql_metrics==py_metrics,(sql_metrics,py_metrics)
cur.execute('SELECT SegmentoTCB, COUNT(*), SUM(AtivoTotal_R_mil), SUM(CarteiraCreditoClassificada_R_mil), SUM(LucroLiquido_R_mil) FROM instituicoes GROUP BY SegmentoTCB ORDER BY SegmentoTCB')
segment_metrics=cur.fetchall()
cur.execute('SELECT COUNT(DISTINCT CodigoInstituicao), COUNT(DISTINCT DataBase), COUNT(DISTINCT TCB), COUNT(DISTINCT TC_Codigo), COUNT(DISTINCT TI_Codigo) FROM instituicoes')
distinct=cur.fetchone()

validation={'rows':sql_metrics[0],'active_total_R$mil':sql_metrics[1],'credit_R$mil':sql_metrics[2],'equity_R$mil':sql_metrics[3],'net_profit_R$mil':sql_metrics[4],'profitable_institutions':sql_metrics[5],'loss_making_institutions':sql_metrics[6],'distinct_codes':distinct[0],'date_bases':distinct[1],'TCB_categories':distinct[2],'TC_codes':distinct[3],'TI_codes':distinct[4],'segment_breakdown':segment_metrics,'reconciliation':'Python/CSV and SQLite headline totals match exactly'}
(processed/'validacao_sql.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
conn.close()
print(json.dumps(validation,ensure_ascii=False))

