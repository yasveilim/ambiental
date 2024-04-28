from O365 import Account
from O365.drive import Folder
from O365.excel import WorkBook
import typing as t

SCOPES = ['basic', 'onedrive_all', 'sharepoint', 'sharepoint_dl']


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
        >>> from sharepoint import autenticate
        >>> myaccount = autenticate()
        >>> # site example: "https://domain.sharepoint.com/sites/Ambiental/file.xlsx"
        >>> mysite = 'root:sites/Ambiental:/file.xlsx'
        >>> _workbook = load_workbook(account, mysite)
    """

    parent, site, filepath = filepath.split(':')

    sp = account.sharepoint()

    main_dir = sp.get_site(parent, site)

    document_library = main_dir.get_document_library('.')
    file_obj = document_library.get_item_by_path(filepath)
    workbook = WorkBook(file_obj)

    return workbook


def make_dir(account: Account, qdirpath: str) -> Folder:
    """
    Create a SharePoint directory and the required parent directories.

    Args:
        account: The SharePoint account.
        qdirpath (str): The path to the target directory in the library system.

    Returns:
        Folder: The taget directory.

    Raises:
        ValueError: If the qdirpath is not in the correct format.

    Example:
        >>> from sharepoint import autenticate
        >>> myaccount = autenticate()
        >>> # taget directory example: "https://domain.sharepoint.com/sites/Ambiental/path/to/target"
        >>> mysite = 'root:sites/Ambiental:/path/to/target'
        >>> _folder = make_dir(account, mysite)
    """

    parent, site, dirpath = qdirpath.split(':')
    path_chucks = dirpath.split('/')[1:]

    sp = account.sharepoint()
    main_dir = sp.get_site(parent, site)
    doc_library = main_dir.get_document_library('.')
    root_folder = doc_library.get_root_folder()

    for chuck in path_chucks:
        query = [x for x in root_folder.get_items() if x.name == chuck]
        chuck_exists = len(query) == 1

        if len(query) > 1:
            raise ValueError(
                f"The search returned more than one result {query}")

        if not chuck_exists:
            new_dir = root_folder.create_child_folder(chuck)
            root_folder = new_dir
        else:
            root_folder = query[0]

    return root_folder


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
