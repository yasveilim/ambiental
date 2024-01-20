from O365 import Account
from O365.excel import WorkBook, WorkSheet
import typing as t

SCOPES = [
    'basic',
    'onedrive_all'
]


def get_file(account: Account, file_id: str):
    storage = account.storage()
    _drives = storage.get_drives()

    my_drive = storage.get_default_drive()  # or get_drive('drive-id')
    file = my_drive.get_item(file_id)

    return file


def set_range(worksheet: WorkSheet, cell_range: str, values: t.Any):
    celda1 = worksheet.get_range(cell_range)
    celda1.values = values
    celda1.update()


def modify_exel(file):

    excel_file = WorkBook(file)
    ws = excel_file.get_worksheet('Hoja1')
    set_range(ws, 'A1', 37 + 2)


def ls_storage(folder):

    # iterate over the first 25 items on the root folder
    for item in folder.get_items():  # limit=25
        print(item, item.drive_id, item.name)
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
