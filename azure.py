from O365 import Account, FileSystemTokenBackend
from O365.excel import WorkBook


def modify_exel(file_instance):
    # my_file_instance should be an instance of File.
    excel_file = WorkBook(file_instance)

    ws = excel_file.get_worksheet('my_worksheet')
    cella1 = ws.get_range('A1')
    cella1.values = 35
    cella1.update()


def read_by_id(drive, item_id):
    # item_id = 'D1ED06591598D29B!30531'  # Reemplaza con el ID real del archivo Excel

    # Descarga del archivo Excel para trabajar con él localmente
    excel_file = drive.get_item(item_id)
    excel_file.download('archivo_local.xlsx')

    # Aquí puedes agregar el código para modificar el archivo Excel usando una librería como 'openpyxl'
    # Por ejemplo, para agregar una nueva fila con contenido al final de una hoja existente:
    from openpyxl import load_workbook

    wb = load_workbook('archivo_local.xlsx')
    ws = wb.active  # Asume que trabajamos con la primera hoja

    # Agrega contenido a la nueva fila (reemplaza 'Nuevo Contenido' con el contenido real que deseas agregar)
    ws.append(['Nombre', 'Apellidos', 'Edad', 'Dirección', 'Tel', 'Email'])

    # Guarda los cambios en el archivo local
    wb.save('archivo_local.xlsx')

    # Sube el archivo modificado de vuelta a OneDrive
    excel_file.upload('archivo_local.xlsx')

    print("El archivo Excel ha sido actualizado y subido a OneDrive exitosamente.")


def ls_drive_folder(my_drive):
    # get some folders:
    root_folder = my_drive.get_root_folder()
    attachments_folder = my_drive.get_special_folder('attachments')

    # iterate over the first 25 items on the root folder
    for item in root_folder.get_items(limit=100):
        print(f"Nombre: {item.name}: ID: {item.object_id}")

        if item.is_folder:
            # print the first to element on this folder.
            print(list(item.get_items(2)))

        elif item.is_file:

            if item.is_photo:
                print(item.camera_model)  # print some metadata of this photo

            elif item.is_image:
                print(item.dimensions)  # print the image dimensions

            else:
                # regular file:
                print(item.mime_type)


def main():
    # Configuración de las credenciales y el almacenamiento del token
    client_id = 'dfeed389-6e99-4000-91de-3994802a22c1'
    client_secret = 'e794eac2-a297-41d1-80e5-79c9b478db4a'
    token_backend = FileSystemTokenBackend(
        token_path='.', token_filename='o365_token.json')
    # https://onedrive.live.com/edit?id=429D292F48EEBBBB!sacc1c1b40f4b4c6db069493a4f7d52cc&resid=429D292F48EEBBBB!sacc1c1b40f4b4c6db069493a4f7d52cc&cid=429d292f48eebbbb&ithint=file%2Cxlsx&redeem=aHR0cHM6Ly8xZHJ2Lm1zL3gvYy80MjlkMjkyZjQ4ZWViYmJiL0ViVEJ3YXhMRDIxTXNHbEpPazk5VXN3QjFMVDRtRUl0b044ZkNjcG5OU3YyelE_ZT1UUHR3Z24&migratedtospo=true&wdo=2
    # Autenticación con Microsoft Graph
    credentials = (client_id, client_secret)
    account = Account(credentials, token_backend=token_backend)

    # Si no estás autenticado, esto abrirá el proceso de autenticación en tu navegador predeterminado
    if not account.is_authenticated:
        account.authenticate(scopes=['basic', 'onedrive_all'])

    # Acceso a OneDrive y apertura del archivo Excel
    storage = account.storage()
    drive = storage.get_default_drive()

    ls_drive_folder(drive)


if __name__ == '__main__':
    main()
