import random

def generar_numero_6_digitos():
    return random.randint(100000, 999999)

numero_generado = generar_numero_6_digitos()
print(numero_generado)
