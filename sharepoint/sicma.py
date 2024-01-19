from dotenv import load_dotenv
import os
from . import sharepoint
from O365 import Account

WORKSHEETS = ['CRITICAS', 'AIRE Y RUIDO', 'AYR1.2', 'AGUA', 'RESIDUOS', 'RECNAT Y RIESGO', 'OTROS', r'% de Avance']
MATERIALS = [x for x in WORKSHEETS if x not in ['AYR1.2', r'% de Avance']]
ADVANCE_WORKSHEET = r'% de Avance'

# Parse db result example
"""
{
    # Category
    'CRITICAS': {
        # material: [documents]
        'AIRE':  [],
        'RUIDO': []

    }
}
"""

def read_sicma_db(account: Account):
    workbook = sharepoint.load_workbook(account, 'root:sites/Ambiental:/Requerimientos de informacion V22 NDA1.xlsx')
    # print(workbook)

    # 1) Convertir este archivo en un modulo.
    # 2) Ignorar todas las celdas hasta (guiate del indice):
    #   ['MATERIA', 'ID+', 'DOCUMENTO', 'INDISPENSABLE SUBIR A LA NUBE PREVIO A LA AUDITORÍA', 'AVANCE', '', '', 'ARCHIVOS', 'COMENTARIOS', '']
    # Verifica si para las hojas de interes el indice es el mismo que en la hoja de 'CRITICAS'

    # ['AIRE', 1, 'Licencia Ambiental Única o Licencia de funcionamiento (Actualizada)', 1, '', 1, '', '', '', '']
    # ['', 3, 'Cédula de operación (Últimos 2 años). Incluir constancia de recepción, respaldo y diagramas. Incluye reporte RETC', 1, '', 1, '', '', '', ''] 
    # 3) Procesar los datos en forma de diccionario para generar la siguiente estructura:
    # 4) Cuando a la derecha todos los campos están vacios esto indica que es una nota
    # 5) A veces se inicia en la segunda columna
    _x = [
        {
            'material': 'AIRE',
            'documents': [
                ['Licencia Ambiental Única o Licencia de funcionamiento (Actualizada)', True, 'pending', '', ''],
                [
                    'Cédula de operación (Últimos 2 años). Incluir constancia de recepción, respaldo y diagramas. Incluye reporte RETC',
                    True, 'pending', '', '']
            ]
        },
        {
            'material': 'RUIDO',
            'documents': []
        }
    ]

    result = {}

    for sheet in MATERIALS[:1]:
        current_docuements = {}
        material = ''
        all_cells = sharepoint.read_all_cells(workbook, sheet)
        # print('-' * 10, sheet, '-' * 10)

        for row in all_cells[11:]:

            if not any(row[2:]):
                continue  # Is a note

            if len(row[0]) > 0:
                material = row[0]
                
            current_material = current_docuements.get(material)
            if not current_material:
                current_docuements[material] = []
                current_material = current_docuements[material]

            current_material.append(row[2])


        result[sheet] = current_docuements

    import json
    # >>> your_json = '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    # >>> parsed = json.loads(your_json)
    # >>> print(json.dumps(parsed, indent=4))
    # parsed = json.loads(result)
    with open('nota2.txt', mode='w', encoding='utf-8') as file:
        print(json.dumps(result, indent=4), file=file)
    return result


# ['AIRE', 1, 1, 'Licencia Ambiental Única o Licencia de funcionamiento (Actualizada)', 1, 1, '', 0, '', '', '']
# ['', 'RESIDUOS PELIGROSOS', 1, 1, 'Registro como empresa generadora de residuos peligrosos (Actualizado)', 1, 1, 1, 0, '', '', '']
# ['AGUA', 1, 'SOLO PARA ABASTECIMIENTO A TRAVES DE POZO PROFUNDO', '', '', '', '', '', '', '', '']
def main():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = None  # os.getenv('CLIENT_SECRET')
    account = sharepoint.autenticate(client_id, client_secret)
    read_sicma_db(account)


if __name__ == '__main__':
    main()
