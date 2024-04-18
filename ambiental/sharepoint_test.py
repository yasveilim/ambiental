# import sharepoint
from sharepoint import autenticate, sharepoint, sicma
from dotenv import load_dotenv
import os
import json

def pretty_print_json(objeto_json):
    with open("main.json", "w", encoding="utf-8") as file:
        print(json.dumps(objeto_json, indent=4, sort_keys=True, ensure_ascii=False), file=file)

def main():
    load_dotenv()  # TODO: Move this line and create main function
    client_id = os.getenv('CLIENT_ID')
    client_secret = None  # os.getenv('CLIENT_SECRET')

    sicma_db = sicma.SicmaDB()
    data = sicma_db.data['AGUA']
    pretty_print_json(data)
    
    exit()

    account = autenticate(client_id, client_secret, sharepoint.SCOPES)
    sharepoint.make_dir(account, 'root:sites/Ambiental:/Fake/enero2')


if __name__ == '__main__':
    main()
