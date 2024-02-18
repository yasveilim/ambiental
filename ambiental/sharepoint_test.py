#import sharepoint
from sharepoint import autenticate, sharepoint
from dotenv import load_dotenv
import os

# import 

def main():
    load_dotenv()  # TODO: Move this line and create main function
    client_id = os.getenv('CLIENT_ID')
    client_secret = None  # os.getenv('CLIENT_SECRET')

    account = autenticate(client_id, client_secret, sharepoint.SCOPES)
    sharepoint.make_dir(account, 'root:sites/Ambiental:/Fake/enero2')


if __name__ == '__main__':
    main() 