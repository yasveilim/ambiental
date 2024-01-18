from dotenv import load_dotenv
import os
from. import sharepoint
from O365 import Account

WORKSHEETS = ['CRITICAS', 'AIRE Y RUIDO', 'AYR1.2', 'AGUA', 'RESIDUOS', 'RECNAT Y RIESGO', 'OTROS', r'% de Avance']
MATERIALS = [x for x in WORKSHEETS if x not in ['AYR1.2', r'% de Avance']]
ADVANCE_WORKSHEET = r'% de Avance'

def read_sicma_db(account: Account):
    workbook = sharepoint.load_workbook(account, 'root:sites/Ambiental:/Requerimientos de informacion V22 NDA1.xlsx')
    #print(workbook)

    # 1) Convertir este archivo en un modulo.
    # 2) Ignorar todas las celdas hasta (guiate del indice):
    #   ['MATERIA', 'ID+', 'DOCUMENTO', 'INDISPENSABLE SUBIR A LA NUBE PREVIO A LA AUDITORÍA', 'AVANCE', '', '', 'ARCHIVOS', 'COMENTARIOS', '']
    # Verifica si para las hojas de interes el indice es el mismo que en la hoja de 'CRITICAS'

    # ['AIRE', 1, 'Licencia Ambiental Única o Licencia de funcionamiento (Actualizada)', 1, '', 1, '', '', '', '']
    # ['', 3, 'Cédula de operación (Últimos 2 años). Incluir constancia de recepción, respaldo y diagramas. Incluye reporte RETC', 1, '', 1, '', '', '', ''] 
    # 3) Procesar los datos en forma de diccionario para generar la siguiente estructura:
    x = [
        {
            'material': 'AIRE',
            'documents': [
                ['Licencia Ambiental Única o Licencia de funcionamiento (Actualizada)', True, 'pending', '', ''],
                ['Cédula de operación (Últimos 2 años). Incluir constancia de recepción, respaldo y diagramas. Incluye reporte RETC', True, 'pending', '', ''] 
            ] 
        },
        {
            'material': 'RUIDO',
            'documents': []
        }
    ]
    for row in sharepoint.read_all_cells(workbook, 'CRITICAS'):
        print(row)


def main():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret =  None # os.getenv('CLIENT_SECRET') 
    account = sharepoint.autenticate(client_id, client_secret)
    read_sicma_db(account)
    

if __name__ == '__main__':
    main()