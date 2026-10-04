import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / 'data' / 'raw' / 'dados_original.csv'
out_dir = root / 'data' / 'processed'
out_dir.mkdir(parents=True, exist_ok=True)
out = out_dir / 'dados_IFData_2024_limpo.csv'

with source.open('r', encoding='utf-8-sig', newline='') as f:
    rows = list(csv.reader(f, delimiter=';'))

header = rows[0]
# Export from the source includes a trailing delimiter in the header, creating
# an unnamed final column. Keep the 19 meaningful fields.
header = header[:19]
original_header = header[:]
header[1] = 'Código da instituição'
header[2] = 'Nome do conglomerado prudencial'
header[3] = 'Código do conglomerado financeiro'
header[4] = 'Código do conglomerado prudencial'

records = []
ni_cells = 0
for row in rows[1:]:
    # The export appends segment totals/percentages after the institution list.
    # Keep only institution records for the institution-level analysis.
    if len(row) <= 10 or row[10].strip() != '12/2024' or not row[0].strip():
        continue
    row = (row + [''] * 19)[:19]
    for i, value in enumerate(row):
        if value.strip() == 'NI':
            row[i] = ''
            ni_cells += 1
    records.append(row)

with out.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';', lineterminator='\n')
    writer.writerow(header)
    writer.writerows(records)

# Re-open and verify the output structure.
with out.open('r', encoding='utf-8-sig', newline='') as f:
    clean = list(csv.reader(f, delimiter=';'))
assert len(clean) == len(records) + 1
assert len(set(clean[0])) == len(clean[0]) == 19
assert all(len(r) == 19 for r in clean)
assert all(r[10] == '12/2024' for r in clean[1:])
assert all(v != 'NI' for r in clean[1:] for v in r)
assert len({r[0] for r in clean[1:]}) == len(records)

print(f'Arquivo: {out}')
print(f'Registros: {len(records)}')
print(f'Colunas: {len(header)}')
print(f'Células NI convertidas em vazias: {ni_cells}')
print(f'Cabeçalho original duplicado: {original_header[2] == original_header[4]}')
print(f'Validado: {len(clean)-1} linhas de dados, 19 colunas, somente 12/2024')
