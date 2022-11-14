# -*- coding: utf-8 -*-
#
#  login.py
#  
#  Trabajo Práctico Final
#  Algoritmos y Estructuras de Datos I
#  Equipo: Cañete Andrés, Ciardelli Martín, Touris Santiago, Traba Federico, Zarate Lautaro

import os
from snippets.registro import usuario_existe

path_users = './db/usuarios'
usuarios = os.scandir(path_users)

def login():
    intentos = 0
    user = input('\nIngrese su usuario: ')

    if not usuario_existe(user): 
        print('Usuario inexistente.')
        return False

    try:
        with open(f'{path_users}/{user}.txt','rt',encoding='UTF-8') as datos:
            nombre, pw_account = datos.readline().split(';')
                        
            while True:
                pw_input = input('Ingrese la contraseña: ')

                if pw_input != pw_account: 
                    intentos += 1
                    print(f'Contraseña errónea {intentos}/3')
                else: 
                    return nombre 
    
                if intentos == 3: 
                    return False 
                    
    except Exception as e:
        print(f'Ha ocurrido un error: {e}')

