#!/usr/bin/python3

from cocedom import ComprobarCedula


if __name__ == '__main__':
    while True:
        resultado = ComprobarCedula(input('Cédula: '))
        print(f'  Nombre: {resultado["nombre"]}')
        print(f'  Cédula: {resultado["cedula"]}')
