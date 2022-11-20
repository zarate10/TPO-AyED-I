# -*- coding: utf-8 -*-
#
#  fechas.py
#  
#  Trabajo Práctico Final
#  Algoritmos y Estructuras de Datos I
#  Equipo: Cañete Andrés, Ciardelli Martín, Touris Santiago, Traba Federico, Zarate Lautaro

import os 
import datetime 

path_fechas  = './db/fechas'
from snippets.tiempo import es_menor, dias_restantes

def obtener_id(username): 
    """
    Busca en el documento de la ruta especificada la última ID. 
    En caso de encontrarla, la devuelve. 

    Args: 
        - username tipo string.
    return: 
        - entero ID. 
    """

    ultimo_id = 0 # acá guardamos la última ID encontrada

    try: 
        with open(f'{path_fechas}/{username}_fechas.txt', 'rt', encoding="UTF-8") as f_fechas: 

            for linea in f_fechas: 
                ultimo_id = linea.strip().split(";")[0]

    except Exception as e: 
        print('Ocurrió un error:', e)

    return int(ultimo_id)


def obtener_fecha_examen(): 
    """
    Pregunta al usuario una fecha de exámen. Si la fecha es válida (fecha no anterior al día actual), la devuelve.

    return: 
        - tupla con día, mes y año. 
    """

    while True: 
        dia, mes, anio = input('Ingrese fecha (dd-mm-aaaa): ').split('-')
                
        if not es_menor(anio + mes + dia): 
            return dia, mes, anio 

def validar_texto(name_option):
    """
    Pide un string y verifica que este cumpla con las condiciones correspondientes. 
    Si el string es válido, lo devuelve.

    Args:
        - name_option: nombre identificador tipo string. 
    return: 
        - texto validado
    """

    while True: 
        option = input(f'Ingrese {name_option}: ')
        if len(option) > 0 and len(option) < 21 and not ';' in option: 
            return option 

        print(f'"{name_option}" debe contener como maximo 20 caracteres y no debe contener ";"')

def agregar_fecha(username):
    """
    Graba una fecha en el documento del usuario que le pasemos como parámetro.
    La validación de los datos es realizada a través de funciones externas. 

    Args: 
        - nombre de usuario tipo string
    """

    id = 0

    # si el archivo contiene líneas, busscamos la última id y sumamos 1.
    # si no, la id quedará en id = 0. 
    if os.stat(f'{path_fechas}/{username}_fechas.txt').st_size != 0:
        id = obtener_id(username) + 1

    try: 
        with open(f'{path_fechas}/{username}_fechas.txt', 'at', encoding='UTF-8') as fechas: 

            materia = validar_texto('materia')
            instancia = validar_texto('instancia')
            dia, mes, anio = obtener_fecha_examen()

            if not id: 
                fechas.write(f'{id};{dia}-{mes}-{anio};{materia};{instancia}\n')
                return 

            fechas.write(f'{id};{dia}-{mes}-{anio};{materia};{instancia}\n')

    except Exception as e:
        print('Ocurrió un error:', e)

    return

def matriz_fechas(username):
    """
    Busca el archivo de un usuario existente y la traslada a memoria principal para la manipulación a través de un array.

    Args: 
        - nombre de usuario tipo string.
    return: 
        - un array donde cada elemento representa una fecha con su respectivo ID, FECHA MATERIA e INSTANCIA
    """
    try:
        with open(f'{path_fechas}/{username}_fechas.txt', 'rt', encoding='UTF-8') as fechas:
            matriz = [linea.rstrip().split(';') for linea in fechas]
            
    except Exception as e:
        print('Ocurrió un error:', e)

    return matriz

def mostrar_fechas(matriz):
    """
    Printea matriz con formateo. 

    Args: 
        - matriz con las fechas del usuario
    """
    print('{:<2} | {:<10} | {:<15} | {:<20} | {:<15}'.format('ID','Fecha', "Días restantes", 'Materia', 'Instancia'))
    print('-'*85)
    for elem in matriz:
        print('{:<2} | {:<10} | {:<15} | {:<20} | {:<15}'.format(elem[0], elem[1], dias_restantes(''.join(elem[1].split('-')[::-1])), elem[2], elem[3]))
        
    return 

def id_fecha(matriz):
    """
    Solicita una ID al usuario y verifica que esta exista. 
    Si existe, la devuelve.

    Args:
        - matriz con las fechas del usuario 
    return: 
        - id de una fecha específica
    """

    while True: 
        try:
            id = int(input('Ingresar ID: '))
            matriz[id] 
        except IndexError: 
            print('No existe la ID seleccionada.')
        except Exception as e: 
            print('Error: ', e)
        else: 
            return id 


def modificar_fechas(id, matriz, username):
    """
    Permite al usuario modificar la fecha de un exámen a través de la ID. 
    El ID representa el índice de un elemento dentro de la matriz. 
    Si los datos proporcionados son correctos, graba la nueva información.

    Args:
        - id: índice de la fecha correspondiente de la matriz.
        - matriz: matriz con las fechas del usuario.
        - username de tipo string correspondiente al usuario logueado.
    """
 
    fecha = '-'.join(list(obtener_fecha_examen()))
    materia = validar_texto('materia')
    instancia = validar_texto('instancia')

    matriz[id] = [str(id), fecha, materia, instancia] #Cambiamos la linea que desea modificar el usuario

    #Sacamos los datos del archivo e ingresamos la matriz con las actualizaciones del usuario
    try: 
        with open(f'{path_fechas}/{username}_fechas.txt', 'wt', encoding='UTF-8') as fechas:
            [fechas.write(f'{arr[0]};{arr[1]};{arr[2]};{arr[3]}\n') for arr in matriz]
    except Exception as e:
        print('Ocurrió un error:', e) 

    return 

def eliminar_fechas(id, matriz, username):
    """
    Permite al usuario eliminar la fecha de un exámen a través de la ID. 
    El ID representa el índice de un elemento dentro de la matriz. 
    Si los datos proporcionados son correctos, graba la nueva información.

    Args:
        - id: índice de la fecha correspondiente de la matriz.
        - matriz: matriz con las fechas del usuario.
        - username de tipo string correspondiente al usuario logueado.
    """
    matriz.pop(id)

    for i in range(len(matriz)):
        matriz[i][0] = str(i)

    try: 
        with open(f'{path_fechas}/{username}_fechas.txt', 'wt', encoding='UTF-8') as fechas:
            [fechas.write(f'{arr[0]};{arr[1]};{arr[2]};{arr[3]}\n') for arr in matriz]
    except Exception as e:
        print('Ocurrió un error:', e) 

    return 