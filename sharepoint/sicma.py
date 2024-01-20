from dotenv import load_dotenv
import os
from . import sharepoint
from O365 import Account
import typing as t

WORKSHEETS = ['CRITICAS', 'AIRE Y RUIDO', 'AYR1.2', 'AGUA',
              'RESIDUOS', 'RECNAT Y RIESGO', 'OTROS', r'% de Avance']
MATERIALS = [x for x in WORKSHEETS if x not in ['AYR1.2', r'% de Avance']]
ADVANCE_WORKSHEET = r'% de Avance'


def calculate_advance(delivered: str | int, pending: str | int):
    if delivered:
        advance = 'DELIVERED'
    elif pending:
        advance = 'PENDING'
    else:
        advance = 'NA'

    return advance


def extract_row(
        current_docuements: dict,
        row: t.List[str],
        doc_index: int,
        material_idx: int,
        material: str
) -> t.Optional[str]:

    if not any(row[doc_index:]):
        return None

    if len(row[material_idx]) > 0:
        material = row[material_idx]

    current_material = current_docuements.get(material)
    if not current_material:
        current_docuements[material] = []
        current_material = current_docuements[material]

    current_material.append({
        'name': row[doc_index],
        'essential_cloud': bool(row[doc_index + 1]),
        'advance': calculate_advance(row[doc_index + 2], row[doc_index + 3]),
        # ARCHIVES
        'comments': row[-2]
    })

    return material


def read_sicma_db(account: Account):
    workbook = sharepoint.load_workbook(
        account, 'root:sites/Ambiental:/Requerimientos de informacion V22 NDA1.xlsx')

    result = {}
    for sheet in MATERIALS[:2]:
        current_docuements = {}
        material = ''
        all_cells = sharepoint.read_all_cells(workbook, sheet)
        print('-' * 10, sheet, '-' * 10)

        for row in all_cells[11:]:
            print(row)
            # continue
            material_idx = 0
            match sheet:
                case 'CRITICAS':
                    doc_index = 2
                case 'AIRE Y RUIDO':
                    doc_index = 3
                case _: continue  # TODO: raise on unknown sheet

            extract_data = extract_row(
                current_docuements, row, doc_index, material_idx, material
            )

            if extract_data:
                material = extract_data

        result[sheet] = current_docuements

    import json
    # >>> your_json = '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    # >>> parsed = json.loads(your_json)
    # >>> print(json.dumps(parsed, indent=4))
    # parsed = json.loads(result)
    with open('nota2.txt', mode='w', encoding='utf-8') as file:
        print(json.dumps(result, indent=4), file=file)
    return result


# ['AIRE', 1, 1, 'Licencia Ambiental Única o Licencia de funcionamiento (Actualizada)', 1, 1, '', 0, '', '', '']
# ['', 'RESIDUOS PELIGROSOS', 1, 1, 'Registro como empresa generadora de residuos peligrosos (Actualizado)', 1, 1, 1, 0, '', '', '']
# ['AGUA', 1, 'SOLO PARA ABASTECIMIENTO A TRAVES DE POZO PROFUNDO', '', '', '', '', '', '', '', '']
def main():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = None  # os.getenv('CLIENT_SECRET')
    account = sharepoint.autenticate(client_id, client_secret)
    read_sicma_db(account)


if __name__ == '__main__':
    main()
