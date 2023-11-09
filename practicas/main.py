# Importar la clase Account de O365
from O365 import Account, FileSystemTokenBackend

def ls_storage(account: Account):
    storage = account.storage()  # here we get the storage instance that handles all the storage options.

    # list all the drives:
    drives = storage.get_drives()

    # get the default drive
    my_drive = storage.get_default_drive()  # or get_drive('drive-id')

    # get some folders:
    root_folder = my_drive.get_root_folder()
    attachments_folder = my_drive.get_special_folder('attachments')

    # iterate over the first 25 items on the root folder
    for item in root_folder.get_items(limit=25):
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

# Uso de PersoApp de Ismael
client_id = 'eaeb7f26-c831-410a-bc77-7a0c5772e58a'
client_secret = None # '-Y68Q~~7FEmeWeDPUfMPAjrQC21IaL~ZFhJsmdc_'
tenant_id = '7edd3a65-3a1c-4e3a-91de-ef14b15a2e1d' # Id. de directorio (inquilino)

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
account = Account(credentials, token_backend=token_backend) # ,

if not account.is_authenticated:  # will check if there is a token and has not expired
    # ask for a login
    # console based authentication See Authentication for other flows
    account.authenticate(scopes=scopes)


ls_storage(account)