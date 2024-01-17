from O365 import Account, FileSystemTokenBackend
from O365.excel import WorkBook
from dotenv import load_dotenv
import typing as t
import os



WORKSHEETS = ['CRITICAS', 'AIRE Y RUIDO', 'AYR1.2', 'AGUA', 'RESIDUOS', 'RECNAT Y RIESGO', 'OTROS', r'% de Avance']
MATERIALS = [x for x in WORKSHEETS if x not in ['AYR1.2', r'% de Avance']]


def load_workbook(account: Account, filepath: str) -> WorkBook:
    """
    Loads a workbook from a SharePoint document library.

    Args:
        account: The SharePoint account.
        filepath (str): The path to the workbook in the document library.

    Returns:
        WorkBook: The loaded workbook.

    Raises:
        ValueError: If the filepath is not in the correct format.

    Example:
        >>> account = autenticate()
        >>> # site example: "https://domain.sharepoint.com/sites/Ambiental/file.xlsx"
        >>> site = 'root:sites/Ambiental:/file.xlsx'
        >>> workbook = load_workbook(account, site)
    """

    parent, site, filepath = filepath.split(':')

    sp = account.sharepoint()

    main_dir = sp.get_site(parent, site)

    document_library = main_dir.get_document_library('.')
    file_obj = document_library.get_item_by_path(filepath)
    workbook = WorkBook(file_obj)

    return workbook


def get_worksheets_names(workbook: WorkBook) -> t.List[str]:
    """
    Gets the names of all the worksheets in a workbook.

    Args:
        workbook (WorkBook): The workbook to get the names from.

    Returns:
        List[str]: A list with the names of all the worksheets in the workbook.
    """

    worksheets = workbook.get_worksheets()
    worksheet_names = [worksheet.name for worksheet in worksheets]

    return worksheet_names



def read_all_cells(excel_file: WorkBook, worksheet: str) -> t.List[t.List[str]]:
    """
    Reads all the cells in the specified worksheet of the given Excel file.

    Args:
        excel_file (WorkBook): The Excel file to read from.
        worksheet (str): The name of the worksheet to read from.

    Returns:
        List[List[str]]: A list of lists representing the values of all the cells in the worksheet.
    """

    ws = excel_file.get_worksheet(worksheet)
    used_range = ws.get_used_range()

    return used_range.values


def autenticate() -> Account:

    client_id = os.getenv('CLIENT_ID')
    client_secret =  None # os.getenv('CLIENT_SECRET')
    
    credentials = (client_id, client_secret)
    token_backend = FileSystemTokenBackend(
        token_path='.', token_filename='o365_token.json'
    )
    account = Account(credentials, token_backend=token_backend)

    if not account.is_authenticated:
        account.authenticate(
            scopes=['basic', 'onedrive_all', 'sharepoint', 'sharepoint_dl']
        )
    
    return account


def read_sicma_db(account: Account):
    workbook = load_workbook(account, 'root:sites/Ambiental:/Requerimientos de informacion V22 NDA1.xlsx')
    print(workbook)
    print(read_all_cells(workbook))


def main():
    load_dotenv()
    account = autenticate()
    read_sicma_db(account)



if __name__ == '__main__':
    main()