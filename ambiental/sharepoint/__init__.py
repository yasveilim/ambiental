from O365 import Account, FileSystemTokenBackend
import typing as t
from pathlib import Path


def autenticate(
        client_id: str,
        client_secret: t.Optional[str],
        scopes: t.List[str]
) -> Account:
    """
    This function is used to authenticate a user's Office 365 account and return the authenticated account object.

    Args:
        client_id: (str) - The client_id is a string which represents the ID of the client application that is
        registered in Azure Active Directory.
        client_secret: (str) (Optional) - The client_secret is a string that represents the client secret for the
        application registered in Azure Active Directory.
        scopes: (t.List[str]) Required access scopes for authentication.

    Returns:
        Account object - If the authentication is successful, the Account object associated with the authenticated
        session is returned.

    The function follows these steps:
     1. It pairs the client_id and client_secret into a tuple named credentials.
     2. It establishes a FileSystemTokenBackend which is used to manage tokens for persistence in the local file system
        (o365_token.json).
     3. It generates an Account instance using the credentials and the token backend created.
     4. If the Account instance is not authenticated already, it authenticates it using the SHAREPOINT_SCOPES variable
        (which holds the required access scopes).
     5. It finally returns the authenticated Account instance.
    """
    current_dir = Path(__file__).resolve().parent
    credentials = (client_id, client_secret)
    token_backend = FileSystemTokenBackend(
        token_path=current_dir, token_filename='o365_token.json'
    )
    account = Account(credentials, token_backend=token_backend)

    if not account.is_authenticated:
        account.authenticate(scopes=scopes)

    return account
