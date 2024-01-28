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
    critical_materials: t.List[str] = field(default_factory=list)

    def extract_row(self, row: t.List[str]) -> t.Optional[str]:

        if len(row[self.material_idx]) > 0:
            self.material = row[self.material_idx]

        if not any(row[self.doc_index:]):
            return None

        if not self.current_docuements.get(self.material):
            self.current_docuements[self.material] = []

        current_material = self.current_docuements[self.material]

        name = row[self.doc_index]

        current_material.append({
            'name': name,
            'essential_cloud': bool(row[self.doc_index + 1]),
            'advance': calculate_advance(
                row[self.doc_index + 2], row[self.doc_index + 3]),
            'archives': row[-3],
            'comments': row[-2],
            'is_critical': name in self.critical_materials
        })

        return self.material


def read_sicma_db(account: Account):
    workbook = sharepoint.load_workbook(
        account, 'root:sites/Ambiental:/Requerimientos de informacion V22 NDA1.xlsx')

    result = {}
    critical_materials = []
    for sheet in MATERIALS:
        data_extractor = DataExtractor()
        data_extractor.critical_materials = critical_materials
        all_cells = sharepoint.read_all_cells(workbook, sheet)

        for row in all_cells[11:]:
            if sheet == 'AGUA':
                pass

            match sheet:
                case 'CRITICAS':
                    data_extractor.doc_index = 2
                case 'AIRE Y RUIDO' | 'AGUA' | 'RECNAT Y RIESGO' | 'OTROS':
                    data_extractor.doc_index = 3
                case 'RESIDUOS':
                    data_extractor.doc_index = 4
                    data_extractor.material_idx = 1
                case _: raise ValueError(
                    f'The {sheet} material is unknown and it has not been '
                    'possible to assign an accurate extraction strategy.'
                )

            data_extractor.extract_row(row)

        if sheet == 'CRITICAS':
            cc = data_extractor.current_docuements.values()
            for critica in cc:
                critical_materials += [x['name'] for x in critica]

            continue

        result[sheet] = data_extractor.current_docuements

    return result


class SicmaDB:

    def __init__(self):
        load_dotenv()  # TODO: Move this line and create main function
        client_id = os.getenv('CLIENT_ID')
        client_secret = None  # os.getenv('CLIENT_SECRET')

        self.account = autenticate(client_id, client_secret, sharepoint.SCOPES)
        self.data = read_sicma_db(self.account)

