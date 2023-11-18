# Importar la clase Account de O365
from O365 import Account, FileSystemTokenBackend
from O365.excel import WorkBook

def get_file(account: Account, file_id: str):
    storage = account.storage()  # here we get the storage instance that handles all the storage options.

    # list all the drives:
    drives = storage.get_drives()

    # get the default drive
    my_drive = storage.get_default_drive()  # or get_drive('drive-id')

    # get the file by its ID
    file = my_drive.get_item(file_id)

    # return the file instance
    return file

def get_range(worksheet, range, values):
    celda1 = worksheet.get_range('A1')
    celda1.values = values
    celda1.update()

def modify_exel(file):

    excel_file = WorkBook(file)
    ws = excel_file.get_worksheet('Hoja1')
    get_range(ws, 'A1', 37 + 2)
    


def ls_storage(folder):

    # iterate over the first 25 items on the root folder
    for item in folder.get_items(): # limit=25
        print(item, item.drive_id, item.name)
        if item.is_folder:
            print(list(item.get_items(2)))  # print the first to element on this folder.
        elif item.is_file:
            if item.is_photo:
                print(item.camera_model)  # print some metadata of this photo
            elif item.is_image:
                print(item.dimensions)  # print the image dimensions
            else:
                # regular file:
                print(item.mime_type)


def login_azure():

    # Uso de PersoApp de Ismael
    client_id = '1dc3fdea-0a3d-47d1-866d-29b822fbb36e' #'eaeb7f26-c831-410a-bc77-7a0c5772e58a'
    client_secret = None # '-Y68Q~~7FEmeWeDPUfMPAjrQC21IaL~ZFhJsmdc_'
    _tenant_id = '7edd3a65-3a1c-4e3a-91de-ef14b15a2e1d' # Id. de directorio (inquilino)

    # Se necesitan los permisos en la categoria File (en permisos de API)


    # quiero escuchar, es mas quiero escuchar tu voz : (
    # Definir las credenciales de la aplicación registrada en Azure Portal
    credentials = (client_id, client_secret)

    scopes = [
        'basic',
        'onedrive_all'
        # 'Files.Read'
    ]

    token_backend = FileSystemTokenBackend(token_path='my_folder', token_filename='my_token.json')
    # Crear una instancia de la clase Account con las credenciales y el permiso Files.Read
    account = Account(credentials, token_backend=token_backend)

    if not account.is_authenticated:  # will check if there is a token and has not expired
        # ask for a login
        # console based authentication See Authentication for other flows
        account.authenticate(scopes=scopes)

    return account

def main():
    account = login_azure()
    exelfile = get_file(account, 'D1ED06591598D29B!30531')
    modify_exel(exelfile)

if __name__ == '__main__':
    main()