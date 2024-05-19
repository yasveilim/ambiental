from dotenv import load_dotenv
import os
from . import sharepoint, autenticate
from dataclasses import dataclass, field
from O365 import Account
import typing as t
from datetime import datetime
from O365.drive import Folder
from enum import Enum
import uuid

WORKSHEETS = [
    "CRITICAS",
    "AIRE Y RUIDO",
    "AYR1.2",
    "AGUA",
    "RESIDUOS",
    "RECNAT Y RIESGO",
    "OTROS",
    r"% de Avance",
]
MATERIALS = [x for x in WORKSHEETS if x not in ["AYR1.2", r"% de Avance"]]
ADVANCE_WORKSHEET = r"% de Avance"


def calculate_advance(delivered: str | int, pending: str | int):
    if delivered:
        advance = "DELIVERED"
    elif pending:
        advance = "PENDING"
    else:
        advance = "NA"

    return advance


@dataclass
class DataExtractor:
    current_docuements: t.Dict = field(default_factory=dict)
    # This is used to store the last NDA number found in the excel sheet.
    nda_index: t.Optional[int] = None
    last_nda: t.Optional[int] = None
    doc_index: int = 0
    material_idx: int = 0
    material: str = ""
    # This represents the index of the document number in the excel sheet
    # This number is used to identify the document in the company's system.
    no_doc: int = 0
    critical_materials: t.List[str] = field(default_factory=list)

    def extract_row(self, row: t.List[str]) -> t.Optional[str]:
        if self.nda_index is not None:
            current_nda = str(row[self.nda_index]).strip()
            if len(current_nda) > 0:
                self.last_nda = float(current_nda.replace(",", "."))

        if len(row[self.material_idx]) > 0:
            self.material = row[self.material_idx]

        if not any(row[self.doc_index :]):
            return None

        if not self.current_docuements.get(self.material):
            self.current_docuements[self.material] = []

        current_material = self.current_docuements[self.material]

        name = row[self.doc_index]

        current_material.append(
            {
                "name": name,
                "nda": self.last_nda,
                "doc_number": row[self.no_doc],
                "essential_cloud": bool(row[self.doc_index + 1]),
                "advance": calculate_advance(
                    row[self.doc_index + 2], row[self.doc_index + 3]
                ),
                "archives": row[-3],
                "comments": row[-2],
                "is_critical": name in self.critical_materials,
            }
        )

        return self.material


def read_sicma_db(account: Account, dbpath: str):
    workbook = sharepoint.load_workbook(account, dbpath)

    result = {}
    critical_materials = []
    for sheet in MATERIALS:
        data_extractor = DataExtractor()
        data_extractor.critical_materials = critical_materials
        all_cells = sharepoint.read_all_cells(workbook, sheet)

        if "NDA" in all_cells[9]:
            data_extractor.nda_index = all_cells[9].index("NDA")

        for field_name in ["ID+", "ID", "No."]:
            if field_name in all_cells[9]:
                data_extractor.no_doc = all_cells[9].index(field_name)
                break

        for row in all_cells[11:]:
            if sheet == "AGUA":
                pass

            match sheet:
                case "CRITICAS":
                    data_extractor.doc_index = 2
                case "AIRE Y RUIDO" | "AGUA" | "RECNAT Y RIESGO" | "OTROS":
                    data_extractor.doc_index = 3
                case "RESIDUOS":
                    data_extractor.doc_index = 4
                    data_extractor.material_idx = 1
                case _:
                    raise ValueError(
                        f"The {sheet} material is unknown and it has not been "
                        "possible to assign an accurate extraction strategy."
                    )

            data_extractor.extract_row(row)

        if sheet == "CRITICAS":
            cc = data_extractor.current_docuements.values()
            for critica in cc:
                critical_materials += [x["name"] for x in critica]

            continue

        result[sheet] = data_extractor.current_docuements

    return result


class SicmaDB:

    def __init__(self):
        load_dotenv()
        client_id = os.getenv("CLIENT_ID")
        client_secret = None  # os.getenv('CLIENT_SECRET')
        self.site_path = "root:sites/Ambiental:"
        self.account = autenticate(client_id, client_secret, sharepoint.SCOPES)

        db_book = self.site_path_fmt("Requerimientos de informacion V22 NDA1.xlsx")
        self.data = read_sicma_db(self.account, db_book)

    # /{USUARIO}/Informacion IL {Año}/{MATERIAL}/Libros
    def create_material_folder(
        self, dirname: str, material: str, id_book: str, name_book: str
    ) -> Folder:
        # NOTE: year is not an argument because I don't know if it is generated
        # based on the current year or another base.
        year = datetime.now().year
        material_folder = self.site_path_fmt(
            # f"{dirname}/Informacion IL {datetime.now().year}/{material}"
            f"{dirname}/Información Auditoria {year}/{material}/{id_book} {name_book}"
        )
        return sharepoint.make_dir(self.account, material_folder)

    def generate_unique_user_dir(self) -> str:
        random_uuid = uuid.uuid4()

        user_folder_path = self.site_path_fmt(str(random_uuid))
        sharepoint.make_dir(self.account, user_folder_path)

        return random_uuid

    def site_path_fmt(self, *args) -> str:
        path_chucks = "/".join(args)
        return f"{self.site_path}/{path_chucks}"
