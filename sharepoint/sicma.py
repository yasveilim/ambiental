from dotenv import load_dotenv
import os
from . import sharepoint, autenticate
from dataclasses import dataclass, field
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


@dataclass
class DataExtractor:
    current_docuements: t.Dict = field(default_factory=dict)
    doc_index: int = 0
    material_idx: int = 0
    material: str = ""

    def extract_row(self, row: t.List[str]) -> t.Optional[str]:

        if not any(row[self.doc_index:]):
            return None

        if len(row[self.material_idx]) > 0:
            self.material = row[self.material_idx]

        if not self.current_docuements.get(self.material):
            self.current_docuements[self.material] = []

        current_material = self.current_docuements[self.material]

        current_material.append({
            'name': row[self.doc_index],
            'essential_cloud': bool(row[self.doc_index + 1]),
            'advance': calculate_advance(
                row[self.doc_index + 2], row[self.doc_index + 3]),
            'archives': row[-3],
            'comments': row[-2]
        })

        return self.material


def read_sicma_db(account: Account):
    workbook = sharepoint.load_workbook(
        account, 'root:sites/Ambiental:/Requerimientos de informacion V22 NDA1.xlsx')

    result = {}
    for sheet in MATERIALS[:4]:
        data_extractor = DataExtractor()
        all_cells = sharepoint.read_all_cells(workbook, sheet)
        print('-' * 10, sheet, '-' * 10)

        for row in all_cells[11:]:
            print(row)
            # continue

            match sheet:
                case 'CRITICAS':
                    data_extractor.doc_index = 2
                case 'AIRE Y RUIDO' | 'AGUA':
                    data_extractor.doc_index = 3
                case 'RESIDUOS':
                    data_extractor.doc_index = 4
                    data_extractor.material_idx = 1
                case _: continue  # TODO: raise on unknown sheet

            data_extractor.extract_row(row)

        result[sheet] = data_extractor.current_docuements

    import json
    # >>> your_json = '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    # >>> parsed = json.loads(your_json)
    # >>> print(json.dumps(parsed, indent=4))
    # parsed = json.loads(result)
    with open('nota2.txt', mode='w', encoding='utf-8') as file:
        print(json.dumps(result, indent=4), file=file)
    return result


def main():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = None  # os.getenv('CLIENT_SECRET')

    account = autenticate(client_id, client_secret, sharepoint.SCOPES)
    read_sicma_db(account)


if __name__ == '__main__':
    main()
