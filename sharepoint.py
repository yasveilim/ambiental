from O365 import Account, FileSystemTokenBackend
from O365.excel import WorkBook
import typing as t



materials = ['CRITICAS', 'AIRE Y RUIDO', 'AYR1.2', 'AGUA', 'RESIDUOS', 'RECNAT Y RIESGO', 'OTROS', r'% de Avance']


def load_workbook(account, filepath: str) -> WorkBook:
    parent, site, filepath = filepath.split(':')

    sp = account.sharepoint()

    # https://panaserviceperu.sharepoint.com/sites/BOT-PANASERVICE-REGISTRO

    main_dir = sp.get_site(parent, site)

    document_library = main_dir.get_document_library('.')
    file_obj = document_library.get_item_by_path(filepath)
    workbook = WorkBook(file_obj)
    return workbook


def read_all_cells(excel_file):
    worksheets = excel_file.get_worksheets()
    worksheet_names = [worksheet.name for worksheet in worksheets]
    print(worksheet_names)
    
    ws = excel_file.get_worksheet('CRITICAS')
    used_range = ws.get_used_range()
    #print(used_range.values)
    #cells = used_range.get_all_cells()
    for cell in used_range.values:
        print(cell)


def main():
    # Configuración de las credenciales y el almacenamiento del token
    client_id = '683c3232-2013-4131-80fb-cb1285122d05'
    client_secret = None #'3d6198a0-6501-40fc-b40d-426128ffe95a'
    token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.json')
    # https://onedrive.live.com/edit?id=429D292F48EEBBBB!sacc1c1b40f4b4c6db069493a4f7d52cc&resid=429D292F48EEBBBB!sacc1c1b40f4b4c6db069493a4f7d52cc&cid=429d292f48eebbbb&ithint=file%2Cxlsx&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3gvYy80MjlkMjkyZjQ4ZWViYmJiL0ViVEJ3YXhMRDIxTXNHbEpPazk5VXN3QjFMVDRtRUl0b044ZkNjcG5OU3YyelE_ZT1UUHR3Z24&migratedtospo=true&wdo=2
    # Autenticación con Microsoft Graph
    credentials = (client_id, client_secret)
    account = Account(credentials, token_backend=token_backend)

    # Si no estás autenticado, esto abrirá el proceso de autenticación en tu navegador predeterminado
    if not account.is_authenticated:
        account.authenticate(scopes=['basic', 'onedrive_all', 'sharepoint', 'sharepoint_dl'])

    # https://sicmaconsultores.sharepoint.com/sites/Ambiental2/Requerimientos de informacion V22 NDA1.xlsx
    # https://sicmaconsultores.sharepoint.com/sites/Ambiental/Requerimientos de informacion V22 NDA1.xlsx
    # https://sicmaconsultores.sharepoint.com/:x:/r/sites/Ambiental/_layouts/15/Doc.aspx?sourcedoc=%7B3E344534-B11E-4BA3-9557-8AD74B027390%7D&file=Requerimientos%20de%20informacion%20V22%20NDA1.xlsx&action=default&mobileredirect=true
    # Acceso a OneDrive y apertura del archivo Excel
    workbook = load_workbook(account, 'root:sites/Ambiental:/Requerimientos de informacion V22 NDA1.xlsx')
    #sharepoint = account.sharepoint()
    #drive = storage.get_default_drive()
    print(workbook)
    print(read_all_cells(workbook))

if __name__ == '__main__':
    main()