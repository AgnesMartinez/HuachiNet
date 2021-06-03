# This Python file uses the following encoding: utf-8
import math
import random
import re
import sqlite3
import time
from datetime import datetime
import praw
import config
from core import HuachiNet
import traceback
import collections
import operator
import requests
from bs4 import BeautifulSoup
from decimal import *
from misc import diccionario

conn = sqlite3.connect("boveda.sqlite3")

cursor = conn.cursor()

HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

resp_saldo = open("./frases/frases_saldo.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_envio = open("./frases/frases_envio.txt", "r", encoding="utf-8").read().splitlines()

resp_empleado_error = open("./frases/frases_error.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_cuenta = open("./frases/frases_cuenta.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_sinbineros = open("./frases/frases_sinbineros.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_empleado = open("./frases/frases_empleado.txt", "r", encoding="utf-8").read().splitlines()

resp_shop = open("./frases/frases_shop.txt", "r", encoding="utf-8").read().splitlines()

resp_tumbar_cholo = open("./frases/frases_tumbar_cholo.txt", "r", encoding="utf-8").read().splitlines()

resp_tumbar_victima = open("./frases/frases_tumbar_victima.txt", "r", encoding="utf-8").read().splitlines()

resp_seguridad = open("./frases/frases_seguridad.txt", "r", encoding="utf-8").read().splitlines()

resp_autorobo = open("./frases/frases_autorobo.txt", "r", encoding="utf-8").read().splitlines()

resp_levanton = open("./frases/frases_levanton.txt", "r", encoding="utf-8").read().splitlines()

resp_huachilate = open("./frases/frases_huachilate.txt", "r", encoding="utf-8").read().splitlines()

resp_huachibono = open("./frases/frases_huachibono.txt", "r", encoding="utf-8").read().splitlines()

resp_huachiswap = open("./frases/frases_huachiswap.txt","r",encoding="utf-8").read().splitlines()

monaschinas = open("./shop/monaschinas.txt", "r", encoding="utf-8").read().splitlines()

trapos = open("./shop/trapos.txt", "r", encoding="utf-8").read().splitlines()

furros = open("./shop/furro.txt", "r", encoding="utf-8").read().splitlines()

nalgoticas = open("./shop/nalgoticas.txt", "r", encoding="utf-8").read().splitlines()

curas = open("./shop/curas.txt", "r", encoding="utf-8").read().splitlines()

chambeadoras = open("./shop/ganosas.txt", "r", encoding="utf-8").read().splitlines()

galletas = open("./shop/galletas.txt", "r", encoding="utf-8").read().splitlines()

valentines = open("./shop/valentin.txt", "r", encoding="utf-8").read().splitlines()

stonks = diccionario['stonks']

reddit = praw.Reddit(client_id=config.APP_ID, 
                     client_secret=config.APP_SECRET,
                     user_agent=config.USER_AGENT, 
                     username=config.REDDIT_USERNAME,
                     password=config.REDDIT_PASSWORD) 

prohibido = ["Shop","HuachiSwap","Bodega","Huachicuenta"]

vib = ["MarcoCadenas","Empleado_del_mes","Disentibot","AutoModerator"]

def error_log(error):
    """Actualizar el error log"""

    with open("./error_log.txt", "a", encoding="utf-8") as temp_file:
        temp_file.write(error + "\n")

def buscar_log(comment_id):
    """Buscar si el comentario ha sido previamente procesado por el empleado del mes"""

    query = """SELECT * FROM comentarios WHERE id_comment=?"""

    resultado = cursor.execute(query,(comment_id,)).fetchall()

    if resultado != []:
        if comment_id == resultado[0][1]:
            return True
        
    elif resultado == []:
        return False        

def actualizar_log(comment_id):
    """Agregar id de comentarios en el log"""

    query = """INSERT INTO comentarios (id_comment) VALUES (?)"""

    cursor.execute(query,(comment_id,))

    conn.commit()

def saldazo(redditor_id) -> str:
    """Abierto todos los dias de 7am a 10pm"""

    if redditor_id in prohibido:
        return "wow :O chico listo"
    
    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:
        return random.choice(resp_saldo) + f"\n\n{Huachis.saldo_total:,} Huachis + {Huachis.power} unidades de energia 🌀"

def tip(remitente,destinatario,cantidad) -> str:
    """Dar propina por publicaciones y comentarios"""

    if remitente in prohibido:
        return "wow :O chico listo"

    #Acceder a la HuachiNet
    Huachis = HuachiNet(remitente)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(remitente) == False:
        
        return random.choice(resp_tip_cuenta)

    else:
        #Verificar que se tenga saldo suficiente para la transaccion
        if Huachis.saldo_total < cantidad:

            return random.choice(resp_tip_sinbineros)

        else:
            #calcula la edad del destinatario para evitar spam de cuentas recien creadas
            if destinatario == "Empleado_del_mes":
                
                cuenta_dias = 30
            
            else:
                cuenta_dias = edad_cuenta(destinatario)

            if cuenta_dias < 28:

                return "El usuario al que quieres enviar no tiene la madurez suficiente para entrar al sistema, es un pinche mocoso miado, dejalo ahi."

            else:
                #Verificar si el destinatario existe en la HuachiNet
                if Huachis.Verificar_Usuario(destinatario) == False:
                    #Abrimos cuenta y le damos dineros de bienvenida
                    Huachis.Bono_Bienvenida(destinatario)
                
                    reddit.redditor(destinatario).message(diccionario['bienvenida'])
                #Iniciamos transaccion
                Huachis.Enviar_Bineros(destinatario,cantidad)

                if destinatario == "Empleado_del_mes":

                    return random.choice(resp_tip_empleado) + f" [{cantidad} Huachicoin(s) Enviado(s)]"

                elif remitente == "Empleado_del_mes":

                    return "autotip"

                else:
                
                    return random.choice(resp_tip_envio) + f" [{cantidad} Huachicoin(s) Enviado(s)]"

def edad_cuenta(redditor_id) -> int:
    """calcular la edad en dias de la cuenta"""

    cliente =  reddit.redditor(redditor_id).created_utc
    
    f_cuenta = datetime.fromtimestamp(cliente)

    f_hoy = datetime.utcnow()

    diff =  f_hoy - f_cuenta

    return int(diff.days)

def historial(redditor_id) -> list:
    """Revisar el historial de movimientos del cliente"""

    if redditor_id in prohibido:
        return "wow :O chico listo"

    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:

        return (Huachis.historial,Huachis.saldo_total,Huachis.depositos,Huachis.retiros,Huachis.asaltos,Huachis.atracos,Huachis.huachitos,Huachis.premios_huachito,Huachis.levantones,Huachis.perk,Huachis.power,Huachis.trait,Huachis.weapon)

def rank(redditor_id, opcion) -> str:
    """Forbes Mujico - TOP Abinerados"""

    if redditor_id in prohibido:
        return "wow :O chico listo"

    #Acceder a la HuachiNet
    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el redditor tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    ranking = Huachis.Ranking()

    respuesta = "#Forbes Mujico - Top Abinerados\n\nLugar | Mujican@ | Cantidad\n:--|:--:|--:\n"

    for i,item in enumerate(ranking,start=1):

        if opcion == 0:

            if item[0] == redditor_id:

                return f"Tu posicion en la HuachiNet es la numero: __{i}__"
        
        #Respuesta en forma de string
        respuesta += f"__{i}__ | {item[0]} | {item[1]:,} H¢N\n"

        if i == opcion:
            break
                
    return respuesta
 
def buscar_usuario(string):
    """Buscar usuarios para darles un levanton"""

    Huachis = HuachiNet("Empleado_del_mes")

    start = string.index('!levanton')

    cachitos = string[start:].split()

    resultado = ""

    for i,cacho in enumerate(cachitos,start=0):

        if "!levanton" in cacho:

            resultado = cachitos[i+1].replace(',','').replace('.','').replace('/u/','').replace('u/','').strip()
            
            break

    for usuario in Huachis.Mujicanos():

        if resultado.lower() == usuario.lower():

            return usuario

def empleado_del_mes():
    """El motor de nuestra huachieconomia"""

    movimientos = 0       

    #Buscar subreddits
    for subreddit in config.SUBREDDITS:
       
        for comment in reddit.subreddit(subreddit).comments(limit=50):

            #Buscar si el comentario ha sido procesado previamante
            if buscar_log(str(comment.id)) == False:

                #Agregar comentario al log
                actualizar_log(str(comment.id))

                def shop_item(item):

                        compra = shop(str(comment.author),str(comment.parent().author),item)

                        return reddit.redditor(str(comment.author)).message("Ticket de Compra - Shop",compra)

                def shop_huachibono(clase,item):
                    
                        bono = actualizar_huachibonos(str(comment.author),clase,item)

                        return reddit.redditor(str(comment.author)).message("Ticket de Compra - Huachibono",bono)

                texto = comment.body.lower()

                comandos = 0

                for item in texto.split():
                    
                    #No mas de 3 comandos por mono
                    if comandos > 2:
                        break

                    #Buscar comandos
                    if "!tip" in item:

                        if comment.parent().author != None and comment.parent().author != "None":
                            
                            comandos += 1

                            try:
                                #Extraemos la cantidad
                                pattern = '!tip\ *(\d+)'

                                result = re.findall(pattern, texto)

                                cantidad = result[0]

                                #Corroboramos que sea un numero
                                if cantidad.isdigit():

                                    #Realizamos la transaccion
                                    transaccion = tip(str(comment.author),str(comment.parent().author),math.ceil(abs(float(cantidad))))

                                    #Evitar que el empleado se responda a si mismo.
                                    if transaccion == "autotip":
                                        pass
                                    
                                    else:
                                        #Responder al cliente
                                        reddit.redditor(str(comment.author)).message("Transaccion Exitosa",transaccion)

                                        movimientos += 1
                                        
                                            
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                #error_log("Tip -" + traceback.format_exc())

                                movimientos += 1

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                                    
                                
                    elif "!saldazo" in item or "!saldo" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 1
                            #Realizar consulta
                            try:
                                
                                consulta = saldazo(str(comment.author))

                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("Saldazo",consulta)

                                movimientos += 1
                                
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Saldazo -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1
                            
                                                    
                    elif "!rankme" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 1
                            #Realizar consulta
                            try:

                                rankme = rank(str(comment.author),0)

                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("Tu lugar en la HuachiNet",rankme)

                                movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("rankme -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1
                                
                                
                    elif "!rank25" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 1
                            #Realizar consulta
                            try:

                                rank25 = rank(str(comment.author),25)

                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("Forbes Mujico Top 25",rank25)

                                movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("rank25 -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1
                                

                    elif "!rank" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 1
                            #Realizar consulta
                            try:

                                rank10 = rank(str(comment.author),10)

                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("Forbes Mujico Top 10",rank10)

                                movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("rank10" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1
                                                            
                        
                    elif "!shop" in item:

                        if comment.parent().author != None and comment.parent().author != "None":

                            comandos += 3

                            #Opciones del menu
                            opciones = diccionario['opciones shop']
                        
                            for opcion in opciones:

                                if "menu" in texto:
                                    
                                    #Enviar menu
                                    reddit.redditor(str(comment.author)).message(diccionario['menu shop'])
                        
                                    movimientos += 1

                                if opcion in texto:
                                    
                                    #Enviar regalo
                                    shop_item(opcion)

                                    movimientos += 1

                    elif "!huachibono" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 3

                            #huachibonos
                            perks = diccionario['bonos perks']

                            traits = diccionario['bonos traits']

                            weapons = diccionario['bonos weapons']

                            opciones = diccionario['opciones']


                            try:

                                if "menu" in texto:
                                    
                                    #Enviar menu
                                    reddit.redditor(str(comment.author)).message(diccionario['menu bonos']))
                                    
                                    movimientos += 1

                                for opcion in opciones:
                            
                                    if opcion in texto:
                                    
                                        if opcion in perks:

                                            #comprar huachibono
                                            shop_huachibono("perk",perks[opcion])

                                            movimientos += 1

                                        elif opcion in traits:

                                            #comprar huachibono
                                            shop_huachibono("trait",traits[opcion])

                                            movimientos += 1

                                        elif opcion in weapons:

                                            #comprar huachibono
                                            shop_huachibono("weapon",weapons[opcion])

                                            movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("huachibono" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1

                    
                    elif "!asalto" in item:

                        if comment.parent().author != None and comment.parent().author != "None":

                            comandos += 1

                            #Realizar consulta
                            try:

                                resultado = asalto(str(comment.author),str(comment.parent().author),"asalto")

                                #Responder al cliente
                                comment.reply(resultado)

                                movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Asalto -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1
                                

                    elif "!atraco" in item:

                        if comment.parent().author != None and comment.parent().author != "None":

                            comandos += 1

                            #Realizar consulta
                            try:

                                resultado = asalto(str(comment.author),str(comment.parent().author),"atraco")

                                #Responder al cliente
                                comment.reply(resultado)

                                movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Atraco -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1


                    elif "!levanton" in item:

                        if comment.parent().author != None and comment.parent().author != "None":

                            comandos += 3

                            #Realizar consulta
                            try:

                                victima = buscar_usuario(texto)

                                resultado = asalto(str(comment.author),victima,"levanton")

                                #Responder al cliente
                                comment.reply(resultado)

                                movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                #error_log("Levanton -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1
                                

                    elif "!huachito" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 3

                            #Comprar huachitos
                            try:
                                #Verificar cuantos se van a comprar
                                try:
                                    #Extraemos la cantidad
                                    pattern = '!huachito\ *(\d+)'

                                    result = re.findall(pattern, texto)

                                    cantidad = abs(int(result[0]))

                                except:

                                    cantidad = 1

                                respuesta = "__Rasca y gana con Huachito - Loteria Mujicana__"

                                if cantidad < 31:

                                    movimientos += cantidad

                                    for i in range(cantidad):
                                        
                                        resultado = slots(str(comment.author))

                                        respuesta +=  f"\n\n{resultado}\n\n***"

                                    if cantidad < 6:
                                        #Responder al cliente en comentarios
                                        comment.reply(respuesta)
                                    
                                    else:
                                        #Responder al cliente por DM
                                        reddit.redditor(str(comment.author)).message(f"Compraste {cantidad} huachitos!",respuesta)

                                        
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                #error_log("Huachito -" + traceback.format_exc())
                                
                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1


                    elif "!poker" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 1

                            #Realizar consulta
                            try:

                                resultado = pokermujicano(str(comment.author))

                                #Responder al cliente
                                comment.reply(resultado)

                                movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Poker -" + traceback.format_exc())
                                
                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1


                    elif "!huachilate" in item or "!huachilote" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 3

                            try:
                                #Comprar numero determinado de huachilates en una sola ejecucion.
                                try:
                                    #Extraemos la cantidad
                                    if "!huachilate" in texto:

                                        pattern = '!huachilate\ *(\d+)'

                                    elif "!huachilote" in texto:

                                        pattern = '!huachilote\ *(\d+)'

                                    result = re.findall(pattern, texto)

                                    cantidad = abs(int(result[0]))

                                except:

                                    cantidad = 1

                                if cantidad < 31:

                                    for i in range(int(cantidad)):

                                        compra = huachilate(str(comment.author))

                                    #Responder al cliente
                                    reddit.redditor(str(comment.author)).message(f"Compraste {cantidad} huachilate(s)!",compra)

                                    movimientos += 1

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                #error_log("Huachilate -" + traceback.format_exc())
                                
                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1

                    elif "!rtd" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 1
                            
                            try:
                                #Extraemos la cantidad
                                string = comment.body.lower()
                    
                                pattern = '!rtd\ *(\d+)'

                                result = re.findall(pattern, string)

                                numero = abs(int(result[0]))

                                if numero > 0 and numero < 7:
                                    
                                    #Realizamos la transaccion
                                    resultado = rollthedice(str(comment.author),numero)
                                    
                                    #Responder al cliente
                                    comment.reply(resultado)

                                    movimientos += 1
                                        
                                            
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("RTD -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1
                    
                    elif "!stonks" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 3

                            try:
                              
                                #Realizamos la consulta
                                resultado = consultar_stonks()
                                    
                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("HuachiSwap Liquidity Pool",resultado)

                                movimientos += 1             
                                            
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("stonks -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1

                    elif "!portafolio" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 3

                            try:
                              
                                #Realizamos la consulta
                                resultado = portafolio(str(comment.author))
                                    
                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("HuachiSwap - Portafolio",resultado)

                                movimientos += 1             
                                            
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Portafolio -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1

                    
                    elif "!comprar" in item or "!long" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 3

                            try:
                                #Comprar X cantidad de tokens.

                                comentario = texto.split()
                    
                                for i,item in enumerate(comentario,start=0):

                                    if "!comprar" in item or "!long" in item:

                                        ticker = comentario[i+1]

                                        cantidad = math.ceil(abs(float(comentario[i+2])))

                                        compra = buy(str(comment.author),ticker.upper(),cantidad)

                                        #Responder al cliente
                                        reddit.redditor(str(comment.author)).message("HuachiSwap - Resumen de operacion",compra)

                                        movimientos += 1

                                        break
                            except:

                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Long -" + traceback.format_exc())
                                
                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1


                    elif "!vender" in item or "!short" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 3

                            try:
                                #Vender X cantidad de tokens.

                                comentario = texto.split()

                                for i,item in enumerate(comentario,start=0):

                                    if "!vender" in item or "!short" in item:

                                        ticker = comentario[i+1]

                                        cantidad = math.ceil(abs(float(comentario[i+2])))

                                        venta = sell(str(comment.author),ticker.upper(),cantidad)

                                        #Responder al cliente
                                        reddit.redditor(str(comment.author)).message("HuachiSwap - Resumen de operacion",venta)

                                        movimientos += 1

                                        break
                            except:

                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Short -" + traceback.format_exc())
                                
                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1

                    elif "!huachiswap" in item:

                        if comment.author != None and comment.author != "None":

                            comandos += 3

                            try:
                                
                                #Enviar X cantidad de tokens.

                                comentario = texto.split()

                                for i,item in enumerate(comentario,start=0):

                                    if "!huachiswap" in item:

                                        ticker = comentario[i+1]

                                        cantidad = math.ceil(abs(float(comentario[i+2])))
                              
                                        #Realizamos la consulta
                                        resultado = huachiswap(str(comment.author),str(comment.parent().author),ticker.upper(),cantidad)
                                    
                                        #Responder al cliente
                                        reddit.redditor(str(comment.author)).message("HuachiSwap - Transaccion Exitosa",resultado)

                                        movimientos += 1

                                        break             
                                            
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("HuachiSwap -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                                movimientos += 1
    
    return movimientos
                    
def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    for mensaje in reddit.inbox.unread(limit=100):

        if mensaje.author in prohibido:
            pass

        #Buscar si el mensaje ha sido procesado previamante    #Perks 9 a 12
        if buscar_log(str(mensaje.id)) == False:

            try:

                if "!historial" in mensaje.body:

                    #Agregar mensaje al log
                    actualizar_log(str(mensaje.id))

                    print(f'Enviando estado de cuenta: {mensaje.author}')

                    estado_cuenta = historial(str(mensaje.author))

                    asalto_victoria = [item for item in estado_cuenta[4] if int(item[2]) > 0]

                    asalto_perdida = [item for item in estado_cuenta[4] if int(item[2]) < 0]

                    atraco_victoria = [item for item in estado_cuenta[5] if int(item[2]) > 0]

                    atraco_perdida = [item for item in estado_cuenta[5] if int(item[2]) < 0] 

                    chunk = diccionario['chunk']

                    for i,item in enumerate(estado_cuenta[0],start=1):

                        chunk += f"{datetime.fromtimestamp(float(item[1])).ctime()} | {item[3]} | {item[2]} | {item[4]}\n"
                        
                        if len(estado_cuenta[0]) < 20:
                            
                            x = len(estado_cuenta[0])

                        else:

                            x = 20
                            
                        if i % x == 0:

                            reddit.redditor(str(mensaje.author)).message(f"Estado de Cuenta: {mensaje.author}",chunk)

                            break
                
            except Exception as e:
                #Mensaje no tienes cuenta
                error_log(e)

                mensaje.reply(random.choice(resp_tip_cuenta))

                movimientos += 1

def shop(remitente,destinatario,regalo):
    """Tienda de regalos"""

    if remitente in prohibido:
        return "wow :O chico listo"

    #Acceder a la HuachiNet
    Huachis = HuachiNet(remitente)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(remitente) == False:
        
        return random.choice(resp_tip_cuenta)

    else:

        cantidad = 10

        if regalo == "huachito":
            
            cantidad = 20
        

        #Verificar que se tenga saldo suficiente para la transaccion
        if Huachis.saldo_total < cantidad:

            return random.choice(resp_tip_sinbineros)

        else:

            #Iniciamos transaccion
            Huachis.Enviar_Bineros('Shop',cantidad,nota=regalo.capitalize())
            
            if regalo == 'monachina':

                monachina = random.choice(monaschinas)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado una mona china! Kawaii desu ne! \n\n [Abrir Regalo]({monachina})")

                return random.choice(resp_shop)

            elif regalo == 'trapo':

                trapo = random.choice(trapos)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado una dama con rama, no tengas miedo papi, si la agarras no da toques. \n\n [Abrir Regalo]({trapo})")

                return random.choice(resp_shop)

            elif regalo == 'furro':

                furro = random.choice(furros)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado un furro, quemalo antes de que se reproduzca! \n\n [Abrir Regalo]({furro})")

                return random.choice(resp_shop)

            elif regalo == 'nalgotica':

                nalgotica = random.choice(nalgoticas)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado una nalgotica, 2spoopy4me \n\n [Abrir Regalo]({nalgotica})")

                return random.choice(resp_shop)

            elif regalo == 'cura':

                cura = random.choice(curas)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado una cura, La cura del Dr. Corvus Beulenpest es la mejor! \n\n [Abrir Regalo]({cura})")

                return random.choice(resp_shop)

            elif regalo == 'chambeadora':

                chambeadora = random.choice(chambeadoras)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado una chambeadora, Revisas fogosas, pura picardia mexicana con el clasico sexismo de la epoca!\n\n [Abrir Regalo]({chambeadora})")

                return random.choice(resp_shop)
              
            elif regalo == 'galleta':

                galleta = random.choice(galletas)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado una galleta de la suerte. ¿Cuál será tu fortuna? \n\n {galleta}")

            elif regalo == 'huachito':

                huachito = slots(destinatario,regalo=True)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado un huachito, que te diviertas rascando! \n\n {huachito}")

                return random.choice(resp_shop)

            elif regalo == 'valentin':

                valentin = random.choice(valentines)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado una tarjeta de San Valentín! \n\n [Abrir Regalo]({valentin})")

                return random.choice(resp_shop)

def asalto(cholo,victima,tipo):
    """Saca bineros morro"""

    if victima == 'None' or victima == None:

        return "Patron, me parece que esa persona no existe."

    if victima in prohibido or cholo in prohibido:
        return "wow :O chico listo"

    if cholo == victima:
        #Respuesta en caso de autorobo

        if cholo == "Empleado_del_mes":
            pass

        else:

            return random.choice(resp_autorobo)

    #Proteger a los bots
    if victima in vib:
        
        return random.choice(resp_seguridad)

    else:

        #Acceder a cuentas
        huachis_cholo = HuachiNet(cholo)

        perks_cholo = [perk for perk in huachis_cholo.Consultar_Perks() if isinstance(perk,int) == False]

        huachis_victima = HuachiNet(victima)

        #Primero verificar que la victima tenga una cuenta
        if huachis_victima.Verificar_Usuario(victima) == False:
        
            return "No tiene cuenta, dime, que piensas robarle, ¿Los calzones?"

        perks_victima = [perk for perk in huachis_victima.Consultar_Perks() if isinstance(perk,int) == False ]

        #Mensajes personalizados para huachibonos de proteccion        
        if huachis_cholo.trait == "Marika" or huachis_victima.trait == "Marika":

            return "Que es ese olor, __sniff sniff__ huele a que alguien compro el huachibono de 'mArIKa'. Salio mod y no quiere que lo roben, pero tampoco puede robar."

        if huachis_victima.trait == "Vacuna":

            return "Esta persona ha sido inyectada con Patria! la vacuna mujicana, los efectos secundarios la volvieron inmune a los robos, dejame decirte que ya valiste madre F"

        if huachis_victima.perk == "Seguro para la 3era edad":

            if edad_cuenta(victima) > edad_cuenta(cholo):

                #Verificar que tenga energia
                if huachis_victima.power > 4:

                    huachis_victima.Consumir_Energia(5)

                    return "Esta cuenta tiene seguro activo contra maricanuebos, esperate a que se le acabe la vigencia para poderlo robar"

        if huachis_victima.perk == "Barrera Susana Distancia":

            #Verificar que tenga energia
            if huachis_victima.power > 4:

                huachis_victima.Consumir_Energia(5)

                return "Esta cuenta tiene la proteccion de susana distancia! Espera a que se le termine el efecto."

        #calcular monto a jugar

        if tipo == "asalto":

            cantidad_inicial = random.randint(50,500) 

        if tipo == "atraco":

            cantidad_inicial = round((int(huachis_victima.saldo_total) * random.randint(5,16)) / 100)

        if tipo == "levanton":

            cantidad_inicial = round((int(huachis_victima.saldo_total) * 16) / 100)


        cantidad_final = cantidad_inicial

        #Ajustar odds segun huachibonos

        redditor_cholo = huachibonos(cholo)

        redditor_victima = huachibonos(victima)


        if redditor_cholo[0] > redditor_victima[0]:

            #Calcular monto final
            cantidad_final += round((cantidad_inicial * redditor_cholo[1]) / 100) 
                
            cantidad_final += round((cantidad_inicial * redditor_victima[2]) / 100)


            #Verificar que se tenga saldo suficiente para la transaccion
            if huachis_victima.saldo_total < cantidad_final:

                return "Chale, asaltaste a alguien sin dinero suficiente, mal pedo."
            
            else:

                if huachis_victima.Verificar_Usuario(cholo) == False:
                    #Abrimos cuenta y le damos dineros de bienvenida
                    huachis_victima.Bono_Bienvenida(cholo)
                
                    reddit.redditor(cholo).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")
                
                #Enviar Binero
                huachis_victima.Enviar_Bineros(cholo,cantidad_final,nota=tipo.capitalize())

                return random.choice(resp_tumbar_cholo) + f"\n\n__{cholo} ganó {cantidad_final} huachis (de la cartera de {victima})__\n\nBuild | 🌀 | 🎭 | ⚔️\n:--|:--:|:--:|:--:\n{cholo} | {perks_cholo[0]} | {perks_cholo[1]} | {perks_cholo[2]}\n{victima} | {perks_victima[0]} | {perks_victima[1]} | {perks_victima[2]}" 

        else:

            #Primero verificar que el remitente tenga una cuenta
            if huachis_cholo.Verificar_Usuario(cholo) == False:
        
                return random.choice(resp_tip_cuenta)

            else:

                #Calcular el monto final

                cantidad_final += round((cantidad_inicial * redditor_victima[1]) / 100) 
                
                cantidad_final += round((cantidad_inicial * redditor_cholo[2]) / 100)

                #Verificar que se tenga saldo suficiente para la transaccion
                if huachis_cholo.saldo_total < cantidad_final:

                    return "Perdiste, pero no tienes dinero que dar."
            
                else:

                    if huachis_cholo.Verificar_Usuario(victima) == False:
                        #Abrimos cuenta y le damos dineros de bienvenida
                        huachis_cholo.Bono_Bienvenida(victima)
                
                        reddit.redditor(victima).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el post sticky en Mujico para mas informacion de como usar la red.\n\nAqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: \n\n!historial o !saldo / !saldazo")
                
                    #Enviar Binero
                    huachis_cholo.Enviar_Bineros(victima,cantidad_final,nota=tipo.capitalize())

                    return random.choice(resp_tumbar_victima) + f"\n\n__{victima} ganó {cantidad_final} huachis (de la cartera de {cholo})__\n\nBuild | 🌀 | 🎭 | ⚔️\n:--|:--:|:--:|:--:\n{cholo} | {perks_cholo[0]} | {perks_cholo[1]} | {perks_cholo[2]}\n{victima} | {perks_victima[0]} | {perks_victima[1]} | {perks_victima[2]}"

def slots(redditor_id,regalo=False):
    """Ahora si es todo un casino"""

    respuestas_bomba = ["Como en buscaminas, te explotaron las bombas, perdiste!","Varias bombas werito, perdiste","BOMBA! mala suerte :'(","Te salio el negrito y el prietito del arroz, perdistes."]
    
    respuestas_perdida = ["Sigue participando","Suerte para la proxima","Asi es el negocio de rascar boletitos, llevate un dulce del mostrador","Ni pepsi carnal", "Asi pasa cuando sucede","No te awites niño chillon"]

    if redditor_id in prohibido:
        return "wow :O chico listo"

    if regalo != True:

        #Acceder a cuenta del redditor
        Huachis_redditor = HuachiNet(redditor_id)
        
        #Verificar que tenga cuenta
        if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
            return random.choice(resp_tip_cuenta)

        else: 
            #Verificar que tenga saldo
            if Huachis_redditor.saldo_total < 20:
            
                return random.choice(resp_tip_sinbineros)

            else:
                #Cobrar el Huachito
                Huachis_redditor.Enviar_Bineros("Shop",20,nota="Huachito")

    emojis = ['👻','🐷','🐧','🦝','🍮', '💣','👾','👽','🦖','🥓','🤖']

    premios = {}
    premios['👻👻👻'] = 100
    premios['👻👻👻👻'] = 900
    premios['👻👻👻👻👻'] = 5000
    premios['🦖🦖🦖'] = 90
    premios['🦖🦖🦖🦖'] = 800
    premios['🦖🦖🦖🦖🦖'] = 4500
    premios['🦝🦝🦝'] = 80
    premios['🦝🦝🦝🦝'] = 700
    premios['🦝🦝🦝🦝🦝'] = 4000
    premios['🍮🍮🍮'] = 70
    premios['🍮🍮🍮🍮'] = 600
    premios['🍮🍮🍮🍮🍮'] = 3500
    premios['👾👾👾'] = 60
    premios['👾👾👾👾'] = 500
    premios['👾👾👾👾👾'] = 3000
    premios['🐷🐷🐷'] = 50
    premios['🐷🐷🐷🐷'] = 400
    premios['🐷🐷🐷🐷🐷'] = 2500
    premios['🐧🐧🐧'] = 40
    premios['🐧🐧🐧🐧'] = 300
    premios['🐧🐧🐧🐧🐧'] = 2000
    premios['👽👽👽'] = 30
    premios['👽👽👽👽'] = 200
    premios['👽👽👽👽👽'] = 1500
    premios['🤖🤖🤖'] = 20
    premios['🤖🤖🤖🤖'] = 100
    premios['🤖🤖🤖🤖🤖'] = 1500
    premios['🥓🥓🥓🥓🥓'] = 10000

    huachito = [random.choice(emojis) for i in range(5)]

    conteo = collections.Counter(huachito)

    comodin = False

    cantidad_ganada = 0

    if '💣' in conteo and conteo['💣'] > 1:

        #Enviar mensaje de perdida en caso de 2 o mas bombas    
        return f">!{'   '.join(huachito)}!<\n\n>!{random.choice(respuestas_bomba)}!<"

    emoji_mas_repetido = max(conteo.items(), key=operator.itemgetter(1))[0]
    
    #Contar cuantos tocinos hay en el huachito
    if '🥓' in conteo and conteo['🥓'] !=5:

        conteo_tocino = conteo['🥓']

        if emoji_mas_repetido == '🥓':

            conteo.pop('🥓')

            emoji_mas_repetido = max(conteo.items(), key=operator.itemgetter(1))[0]

        comodin = True

        conteo[emoji_mas_repetido] += conteo_tocino

    #Entregar premios
    numero_de_emojis_iguales = conteo[emoji_mas_repetido]

    combinacion = emoji_mas_repetido * numero_de_emojis_iguales

    cantidad_ganada =  premios[combinacion] if combinacion in premios else 0

    

    if cantidad_ganada :

        if '💣' in conteo:
            cantidad_ganada = cantidad_ganada / 2

        cantidad_ganada = int(cantidad_ganada)

        #Acceder a cuenta shop
        Huachis_shop = HuachiNet("Shop")

        #En caso de regalo, verificamos que el destinatario tenga cuenta.
        if regalo == True and Huachis_shop.Verificar_Usuario(redditor_id) == False:
            #Abrimos cuenta y le damos dineros de bienvenida
            Huachis_shop.Bono_Bienvenida(redditor_id)
                
            reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")            
            
        Huachis_shop.Enviar_Bineros(redditor_id,cantidad_ganada,nota="Premio Huachito")

        if comodin:
            mensaje = f">!{'   '.join(huachito)}!<\n\n>!Ganaste {cantidad_ganada:,} huachis ({numero_de_emojis_iguales} iguales usando comodin 🥓)!<"
        else:
            mensaje =  f">!{'   '.join(huachito)}!<\n\n>!Ganaste {cantidad_ganada:,} huachis ({numero_de_emojis_iguales} iguales)!<"
    else:
        mensaje = f">!{'   '.join(huachito)}!<\n\n>!{random.choice(respuestas_perdida)}!<"

    return mensaje

def pokermujicano(redditor_id):

    if redditor_id in prohibido:
        return "wow :O chico listo"

    #Acceder a cuenta del redditor
    Huachis_redditor = HuachiNet(redditor_id)
        
    #Verificar que tenga cuenta
    if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else: 
        #Verificar que tenga saldo
        if Huachis_redditor.saldo_total < 200:
            
            return random.choice(resp_tip_sinbineros)

        else:
            #Cobrar la entrada
            cantidad = random.randint(20,200)
            Huachis_redditor.Enviar_Bineros("Shop",cantidad,nota="Poker")
            
    pot = cantidad * 2

    palos = ["espada","diamante","corazon","trebol"]

    valores = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    baraja = [[('♠',valor,"espada") for valor in valores],
              [('♥',valor,"corazon") for valor in valores],
              [('♦',valor,"diamante") for valor in valores],
              [('♣',valor,"trebol") for valor in valores]]

    cartas = [carta for palo in baraja for carta in palo]

    for i in range(100):
        random.shuffle(cartas)

    manos = random.sample(cartas,k=10)

    mano_casa = manos[0:5]

    mano_redditor = manos[5:10]

    casa = combinaciones_poker(mano_casa)

    redditor = combinaciones_poker(mano_redditor)

    cartas_casa = f'{mano_casa[0][0]} : {mano_casa[0][1]} | {mano_casa[1][0]} : {mano_casa[1][1]} | {mano_casa[2][0]} : {mano_casa[2][1]} | {mano_casa[3][0]} : {mano_casa[3][1]} | {mano_casa[4][0]} : {manos[4][1]}'

    cartas_redditor = f'{mano_redditor[0][0]} : {mano_redditor[0][1]} | {mano_redditor[1][0]} : {mano_redditor[1][1]} | {mano_redditor[2][0]} : {mano_redditor[2][1]} | {mano_redditor[3][0]} : {mano_redditor[3][1]} | {mano_redditor[4][0]} : {mano_redditor[4][1]}'


    #Victoria: Empleado_del_mes
    if casa[0][1] > redditor[0][1]:

        return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para el empleado, con {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

    #Victoria: Redditor
    elif casa[0][1] < redditor[0][1]:

        #Acceder a la cuenta de la shop
        Huachis_shop = HuachiNet("Shop")

        Huachis_shop.Enviar_Bineros(redditor_id,pot,nota="Poker")
        
        return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para {redditor_id}, con {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

    #Empate tecnico, desempate segun combinacion (4 escenarios)
    elif casa[0][1] == redditor[0][1]:

        letras = {"K":13,"A":14,"J":11,"Q":12}

        if casa[2] in palos or redditor[2] in palos:
            #Escenario 1 - Palo que provoco escalera color, color
            carta_alta_casa = [carta[1] for carta in mano_casa if carta[2] == casa[2]]
        
            carta_alta_redditor = [carta[1] for carta in mano_redditor if carta[2] == redditor[2]]

            if carta_alta_casa[0].isdigit() == False:

                carta_alta_casa = [valor for letra,valor in letras.items() if letra == carta_alta_casa[0]]

            if carta_alta_redditor[0].isdigit() == False:

                carta_alta_redditor = [valor for letra,valor in letras.items() if letra == carta_alta_redditor[0]]

            if int(carta_alta_casa[0]) > int(carta_alta_redditor[0]):

                return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para el empleado, usando {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

            elif int(carta_alta_casa[0]) < int(carta_alta_redditor[0]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(redditor_id,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para {redditor_id}, usando {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

            elif int(carta_alta_casa[0]) == int(carta_alta_redditor[0]):

                return f"_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nEmpate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste\n\n_Pot: {pot} huachicoins_"
        
        #Escenario 2 - ambas manos tienen digito como carta alta
        elif casa[2].isdigit() and redditor[2].isdigit():
            
            if int(casa[2]) > int(redditor[2]):

                return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para el empleado, usando {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

            elif int(casa[2]) < int(redditor[2]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(redditor_id,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para {redditor_id}, usando {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

            elif int(casa[2]) == int(redditor[2]):

                return f"_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nEmpate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste\n\n_Pot: {pot} huachicoins_"
        
        #Escenario 3 -Ambas manos tiene carta alta
        elif casa[2] == "None" and redditor[2] == "None": 
            #El valor de la carta mas alta
            if max(casa[1]) > max(redditor[1]):

                return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para el empleado, usando {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

            elif max(casa[1]) < max(redditor[1]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(redditor_id,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para {redditor_id}, usando {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

            elif max(casa[1]) == max(redditor[1]):

                return f"_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nEmpate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste\n\n_Pot: {pot} huachicoins_"        

        #Escenario 4 - Una mano tiene digito como carta alta, la otra tiene letra
        else:

            carta_alta_casa = casa[2]

            carta_alta_redditor = redditor[2]

            if carta_alta_casa[0].isdigit() == False and carta_alta_casa != "None":

                carta_alta_casa = [valor for letra,valor in letras.items() if letra == carta_alta_casa[0]]

            if carta_alta_redditor[0].isdigit() == False and carta_alta_redditor != "None":

                carta_alta_redditor = [valor for letra,valor in letras.items() if letra == carta_alta_redditor[0]]

            if int(carta_alta_casa[0]) > int(carta_alta_redditor[0]):

                return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para el empleado, usando {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

            elif int(carta_alta_casa[0]) < int(carta_alta_redditor[0]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(redditor_id,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para {redditor_id}, usando {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

            elif int(carta_alta_casa[0]) == int(carta_alta_redditor[0]):

                return f"_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nEmpate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste\n\n_Pot: {pot} huachicoins_"
                
def combinaciones_poker(mano):
    """Revisar mano y otorgar un puntaje"""

    #Valores de las cartas
    palos = ["diamante","corazon","trebol","espada"]

    valores = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    #Separar cada tupla en 2 elementos y convertir letras en su valor entero
    palos_cartas = tuple([carta[2] for carta in mano])

    valores_cartas = tuple([carta[1] for carta in mano])

    valores_corregidos = list()

    for valor in valores_cartas:

        if valor.isdigit():
            valores_corregidos.append(int(valor))

        elif valor == "A" and "2" in valores_cartas and "3" in valores_cartas and "4" in valores_cartas and "5" in valores_cartas:
            valores_corregidos.append(1)
        
        elif valor == "A":
            valores_corregidos.append(14)

        elif valor == "J":
            valores_corregidos.append(11)

        elif valor == "Q":
            valores_corregidos.append(12)

        elif valor == "K":
            valores_corregidos.append(13)

    #Evaluar mano segun combinaciones en orden descendente, puntaje minimo es 1 (carta alta)
    #Escalera real de color / escalera de color / color
    for palo in palos:
        if palos_cartas.count(palo) == 5:
            if "A" in valores_cartas and "K" in valores_cartas and "Q" in valores_cartas and "J" in valores_cartas and "10" in valores_cartas:
                #Puntaje Escalera real de color
                puntaje = ("escalera real de color",10)

                return (puntaje,valores_corregidos,"None")
        
            else:
                #Contar numeros consecutivos
                escalera_color = 0

                cartas = sorted(valores_corregidos,reverse=True)

                for i in range(5):

                    if i == 4:
                        break

                    else:
                        
                        if cartas[i] - cartas[i+1] == 1:
                        
                            escalera_color += 1 
                
                if escalera_color == 4:
                    #Puntaje Escalera de color
                    puntaje = ("escalera de color",9)

                    return (puntaje,valores_corregidos,palo)
                
                else:
                    #Puntaje Color
                    puntaje = ("color",6)

                    return (puntaje,valores_corregidos,palo)

    #Full House 
    fullhouse = 0
    valor_tercia = ""
    for valor in valores:

        if valores_cartas.count(valor) == 3:
            fullhouse += 3
            valor_tercia = valor
        
        elif valores_cartas.count(valor) == 2:
            fullhouse += 2

    if fullhouse == 5:
        #Puntaje Fullhouse
        puntaje = ("full house",7)

        return (puntaje,valores_corregidos,valor_tercia)

    #Escalera
    #Contar numeros consecutivos
    escalera = 0
    #Escalera alta con A
    if "A" in valores_cartas and "K" in valores_cartas and "Q" in valores_cartas and "J" in valores_cartas and "10" in valores_cartas:
        #Puntaje escalera alta
        puntaje = ("escalera Alta",5)

        return (puntaje,valores_corregidos,"None")

    else:    

        for i in range(5):

            cartas = sorted(valores_corregidos,reverse=True)

            if i == 4:
                break

            else:

                if cartas[i] - cartas[i+1] == 1:
                        
                    escalera += 1
                
        if escalera == 4:
            #Puntaje escalera
            puntaje = ("escalera",5)

            return (puntaje,valores_corregidos,"None")

    #Poker / Tercia / Dos pares / Pares
    pares = 0
    valor_varios = ""
    for valor in valores:
        if valores_cartas.count(valor) ==  4:
            #Poker
            puntaje = ("poker",8)
            valor_varios = valor

            return (puntaje,valores_corregidos,valor_varios)

        if valores_cartas.count(valor) ==  3:
            #Tercia
            puntaje = ("tercia",4)
            valor_varios = valor

            return (puntaje,valores_corregidos, valor_varios)

        if valores_cartas.count(valor) ==  2:
            #Sumar par
            pares += 1
            valor_varios = valor

    if pares == 2:
        #Puntaje dos pares
        puntaje = ("dos Pares",3)

        return (puntaje,valores_corregidos, valor_varios)
    
    elif pares == 1:
        #Puntaje pares
        puntaje = ("par",2)
        
        return (puntaje,valores_corregidos,valor_varios)
    
    puntaje = ("carta alta",1)

    return (puntaje,valores_corregidos,"None")

def huachilate(redditor_id):
    """Vengase y agarre su !huachilote"""

    if redditor_id in prohibido:
        return "wow :O chico listo"

    #Acceder a cuenta del redditor
    Huachis_redditor = HuachiNet(redditor_id)
        
    #Verificar que tenga cuenta
    if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else: 
        #Verificar que tenga saldo
        if Huachis_redditor.saldo_total < 50:
            
            return random.choice(resp_tip_sinbineros)

        else:
            #Cobrar la entrada
            Huachis_redditor.Enviar_Bineros("Huachicuenta",50,nota="Huachilate")

            huachiclave = Huachis_redditor.Huachiclave()

            valores = (time.time(),redditor_id,huachiclave[1])
            
            conn.execute("""INSERT INTO boletitos (timestamp,usuario,huachiclave) VALUES (?,?,?)""",valores)

            conn.commit()

            huachicuenta = HuachiNet("Huachicuenta")

            if huachicuenta.saldo_total >= huachiclave[2]:
                premio_huachilate()

            return random.choice(resp_huachilate)

def premio_huachilate():
    """Repartir premios del huachilate"""

    huachicuenta = HuachiNet("Huachicuenta")

    huachiclave = huachicuenta.Huachiclave()

    participantes = [usuario[0] for usuario in cursor.execute("""SELECT usuario FROM boletitos WHERE huachiclave = ?""",(huachiclave[1],)).fetchall()]

    ganadores = set(random.sample(participantes,k = 50))

    ganadores = list(ganadores)

    premios = [round((huachicuenta.saldo_total * 50 ) / 100),round((huachicuenta.saldo_total * 30 ) / 100),round((huachicuenta.saldo_total * 20 ) / 100)]

    #Entregar premios
    #Primer lugar 50%
    huachicuenta.Enviar_Bineros(ganadores[0],premios[0],nota="Premio Huachilate")

    reddit.redditor(ganadores[0]).message("Felicidades! Primer lugar en Huachilate!",f"Ganaste el huachilote :D\n\nTu premio es de: {premios[0]} huachis, agarralo mientras te dure!")

    #Segundo lugar 30%
    huachicuenta.Enviar_Bineros(ganadores[1],premios[1],nota="Premio Huachilate")

    reddit.redditor(ganadores[1]).message("Felicidades! Segundo lugar en Huachilate!",f"Ganaste el huachilote :D\n\nTu premio es de: {premios[1]} huachis, agarralo mientras te dure")

    #Tercer lugar 20%
    huachicuenta.Enviar_Bineros(ganadores[2],premios[2],nota="Premio Huachilate")

    reddit.redditor(ganadores[2]).message("Felicidades! Tercer lugar en Huachilate!",f"Ganaste el huachilote :D\n\nTu premio es de: {premios[2]} huachis, agarralo mientras te dure")

    #Publicaren reddit

    fecha_huachilote = datetime.fromtimestamp(float(huachiclave[0])).ctime()

    selftext = f"Los ganadores de este Huachilote, con fecha y hora de {fecha_huachilote}　 　　　　　　　　　　 ✦ 　　　　   　 　　　˚　　　　　　　　　　　　　　*　　　　　　   　　　　　　　　　　　　　　　.　　　　　　　　　　　　　　. 　　      💫 　　　　　　　 ✦              🌝  　　　　 　　　　　 🌠 　                                               \n\n👻  ,　　   　.　　　　　　　　　　　　　.　　　ﾟ　  　　　.　　　　　　　　　　　　　.   ,　　　　　　.　　　　　　 ☀                                                🌞  　　　　　           ☄        . 　　　　　　　　　　.　　　　　　　　　      👽　　      　　. 　　　　　　,　　  　　　　.　　　　　　 ☀                                  　 ☄ 　　　    　　✦\n\n    1er | {ganadores[0]} | {premios[0]:,} huachis\n\n✦ 　   　　　,　　　　　　　　　🚀 　　　　 　　,　　　 ‍ ‍ ‍ ‍ 　　　　🌠 　　　　　　　　　　　 　 　　　　　　　　　　　˚　　　 　   　　　　,　　    　　　　　　　.　　　                  🛰  　　    　　 　　　　　.　　　　　　　　　　　　.　　　　　　　　　　　　　　　* 　　   　　　　　 ✦ 　　　　　　　  　\n\n🌟 　　 　　　　　　　 　　　　　.　　　　　　　　　　　　　　　　　　.　　　　　    　　. 　 　　　　　.　　　　  🌚                                                             🌠  　　　　　   　　　　　.　　　　　　　　　　　.　　　　　　　　　　   　 ˚　　　          \n\n👽 　　　　ﾟ　　　　　.　　　                             　　                      🛸 　　　　　　　　　　. 　　 　                            🌎 ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍             ,　 　　　　　            　　*.　　　　　 　　　　.　　　　　　　　　　 ✦ 　　　˚　　　　　　*　👾\n\n    2do | {ganadores[1]} | {premios[1]:,} huachis\n\n. 　. .　　　　　　　　　　 ✦ 　　　　   　 　　　 🛰˚　　　　　　　　　　　　　　*　　　　　　　　　　　　.　　　　　　　　　　　　. 　　 　　　 🌟 　                                   \n\n👾                               ✦ 　　　                         　　 🌠 　　　　　 　 ‍ ‍ ‍ ‍　 　　 ☄ 　　　　　　　　　　,　　   　 　　　　,　　    　　　　　　　　　.　　　  　　    　　　　　 　　　　　.　　　　　　　　　　　　　.　　　　　　　　　　　　　　　* ✦ 　　　　　　　         　        　 👽 　　　 　　 　                     　\n\n ☄ 　　　　　 　　　　　.　　　　　　　　　　　　　　　.　　　　　　　　　　　　　.　　　ﾟ　  　　　.　　　 🛸 　　　　　　　　　 　. ,　　　　　　　.　　　　　　    　　　　🌞 　　　　　　　 　. ☄\n\n    3er | {ganadores[2]} | {premios[2]:,} huachis\n\n✦ 　   　　　,　　　　　　　　　　　              🚀 　　　　 　　,　　　 ‍ ‍ ‍ ‍ 　                     \n\n🌌.　　　　　 　　                              🌟 　　　.　　　　　　　　　　　　　 　　　　　　　　　　　　　˚　　   　　                                  　　,　　　　　 🌝 　　　       　   　                 　　　 🛸 　　　　.　　 　                           \n\n🛰  　　    　　　　　 　　　　　.　　　　　　　　　　　　　.　　　　 👾　　　　　　　　　* 　　   　　　 　　 ✦ 　　　　　　　         　    🌟 .　　　　　　　　　　　　　　　　　　.　　                   🦜 　　. 　 　　                            　.　　　　 \n\n🌚 .　　　　　　　　　　　.　　　　　　　 👽 　　　                                          　🌜ﾟ　　　　　.　　　　　　　　　　　　　　　. 　　 　\n\n🌎 ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ,　 　　　　　　　　　　　　 　　*.　　　　　 　　　　　　　　　　　　　　.　　　　　　　　　　 ✦ 　　　　   　              　　　˚              Felicidades a los ganadores del huachilote　 🛸 　　　　　   　　　　　　　　　　　　　.　　　　　　　　　　　　　　."

    subs = ["Mujico","TechoNegro","memexico"]
    # huachinews flair_id='a0a7193c-579b-11eb-8162-0e6a96a0cacd'
    for sub in subs:

        if sub == "Mujico":

            reddit.subreddit(sub).submit(f'Ganadores del Huachilate serie: "{huachiclave[1]}" :D', selftext=selftext, flair_id='a0a7193c-579b-11eb-8162-0e6a96a0cacd')

        else: 

            reddit.subreddit(sub).submit(f'Ganadores del Huachilate serie: "{huachiclave[1]}" :D', selftext=selftext)

    #Actualizar columna entregado para que se genere nueva huachiclave
    cursor.execute("""UPDATE huachilate SET entregado = 1 WHERE huachiclave = ?""",(huachiclave[1],))

    conn.commit()

def rollthedice(redditor_id,numero):
    """Juego de dados"""

    if redditor_id in prohibido:
        return "wow :O chico listo"

    #Acceder a cuenta del redditor
    Huachis_redditor = HuachiNet(redditor_id)
        
    #Verificar que tenga cuenta
    if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else: 
        #Verificar que tenga saldo
        if Huachis_redditor.saldo_total < 20:
            
            return random.choice(resp_tip_sinbineros)

        else:
            #Cobrar la entrada
            Huachis_redditor.Enviar_Bineros("Shop",20,nota="RollTheDice")

    dados = [('1️⃣',1),('2️⃣',2),('3️⃣',3),('4️⃣',4),('5️⃣',5),('6️⃣',6)]

    dados_lanzados = random.choices(dados,k=3)

    dado_redditor = dados[numero-1]

    conteo = dados_lanzados.count(dado_redditor)

    if random.randint(100,1000) == 777:
        #SUERTUDOTE

        Huachis_redditor.Enviar_Bineros("Shop",1000,nota="777")

        dados_magicos = ['7️⃣','7️⃣','7️⃣']

        return f"*Roll The Dice a la mujicana*\n\nDado de {redditor_id}\n\n#{dado_redditor[0]}\n\nDados lanzados por el empleado:\n\n#{' '.join(dados_magicos)}\n\nFelicidades! aunque....como le hiciste para sacar triple 7......mejor cambio estos dados por unos nuevos\n\nPremio: 1000 huachicoins)"


    if dados_lanzados == [('6️⃣',6),('6️⃣',6),('6️⃣',6)]:
        #2spoopy4me - pierde 50% de su cartera
        cantidad = int(Huachis_redditor.saldo_total) / 2

        Huachis_redditor.Enviar_Bineros("Shop",cantidad,nota="666")

        dados_emoji = [dado[0] for dado in dados_lanzados]

        return f"**Roll The Dice a la mujicana**\n\nDado de {redditor_id}\n\n#{dado_redditor[0]}\n\nDados lanzados por el empleado:\n\n#{' '.join(dados_emoji)}\n\nEsta partida esta embrujada, perdiste la mitad de tu cartera ({cantidad} huachis)"


    elif conteo == 3:
        #Entregar premio 3 dados iguales
        Huachis_shop = HuachiNet("Shop")

        Huachis_shop.Enviar_Bineros(redditor_id,80,nota="Premio RTD")

        dados_emoji = [dado[0] for dado in dados_lanzados]

        return f"**Roll The Dice a la mujicana**\n\nDado de {redditor_id}\n\n#{dado_redditor[0]}\n\nDados lanzados por el empleado:\n\n#{' '.join(dados_emoji)}\n\nVictoria para {redditor_id} con 3 dados iguales!\n\n_Premio: 80 huachis_"

    elif conteo == 2:
        #Entregar premio 3 dados iguales
        Huachis_shop = HuachiNet("Shop")

        Huachis_shop.Enviar_Bineros(redditor_id,60,nota="Premio RTD")

        dados_emoji = [dado[0] for dado in dados_lanzados]

        return f"**Roll The Dice a la mujicana**\n\nDado de {redditor_id}\n\n#{dado_redditor[0]}\n\nDados lanzados por el empleado:\n\n#{' '.join(dados_emoji)}\n\nVictoria para {redditor_id} con 2 dados iguales!\n\n_Premio: 60 huachis_"

    elif conteo == 1:
        #Entregar premio 3 dados iguales
        Huachis_shop = HuachiNet("Shop")

        Huachis_shop.Enviar_Bineros(redditor_id,40,nota="Premio RTD")

        dados_emoji = [dado[0] for dado in dados_lanzados]

        return f"**Roll The Dice a la mujicana**\n\nDado de {redditor_id}\n\n#{dado_redditor[0]}\n\nDados lanzados por el empleado:\n\n#{' '.join(dados_emoji)}\n\nVictoria para {redditor_id} con un dado igual!\n\n_Premio: 40 huachis_"

    dados_emoji = [dado[0] for dado in dados_lanzados]

    resp_dados = ["Suerte para la proxima","No estan cargados, te lo juro","Sigue participando","Hoy no es tu dia","No te awites, niño chillon"]

    return f"**Roll The Dice a la mujicana**\n\nDado de {redditor_id}\n\n#{dado_redditor[0]}\n\nDados lanzados por el empleado:\n\n#{' '.join(dados_emoji)}\n\n_{random.choice(resp_dados)}_"

def huachibonos(redditor_id):
    """Ajusta odds segun configuracion del usuario"""

    #Ajuste para fusca
    if random.randint(1,100) < 10:

        backfire = 20

    else: 

        backfire = 0

    #Ajuste para mariguana azul
    if random.randint(1,100) < 21:
    
        valor = 20

    else:

        valor = 0

    #Cada huachibono representa una tupla con 3 elementos, (mod odds,mod ganancias, mod perdidas), en caso de perk, se agrega un 4 valor: costo energia
    perks = {"Normal":(0,0,0,0),"Barrera Susana Distancia":(0,0,0,5),"Jelatina de BANANA":(20,0,0,5),"Seguro para la 3era edad":(0,0,0,5),"Estampita Detente":(30,0,30,5),"Mariguana roja": (50,-20,0,5),"Mariguana azul": (random.randint(20,50),valor,10,5),"Mariguana dorada": (69,0,30,5)}

    traits = {"Normal":(0,0,0),"Chocomilk": (10,20,0),"Carta Blanca":(0,50,0),"Emulsion Scotch":(20,0,0),"Marika":(0,0,0),"Mariguana verde":(20,10,10),"Salchichas con anticongelante":(0,0,30),"Peste":(0,0,0),"Recargando":(0,0,0),"Vacuna": (80,20,0)}

    weapons = {"Navaja":(0,0,0),"Platano":(random.randint(10,50),0,0),"Florecita de vive sin drogas":(30,0,0),"Rata con thinner":(0,25,0),"Fusca":(20,0,backfire),"Ecayecelocico":(20,0,10)}

    #Ingresar a cuenta del redditor
    Huachis = HuachiNet(redditor_id)
    
    #Odds Base

    if redditor_id in vib:

        puntaje_inicial = 1000
    
    else:

        puntaje_inicial = random.randint(1,100)

    #Odds ajustados
    puntaje_final = puntaje_inicial

    #Ajustes puntaje final segun Perk,Trait y Weapon
    ajuste_perk = perks[Huachis.perk]

    if Huachis.perk != "Normal" or Huachis.perk != "Seguro para la 3era edad" or Huachis.perk != "Barrera Susana Distancia":

        #Verificar que el usuario tenga energia suficiente
        if Huachis.power > ajuste_perk[3]:

            Huachis.Consumir_Energia(ajuste_perk[3])
            
            if ajuste_perk[0] != 0:
        
                puntaje_final += (puntaje_inicial * ajuste_perk[0]) / 100

    ajuste_trait = traits[Huachis.trait]

    if ajuste_trait[0] != 0:
        
        puntaje_final += (puntaje_inicial * ajuste_trait[0]) / 100

    ajuste_weapon = weapons[Huachis.weapon]

    if ajuste_weapon[0] != 0:
        
        puntaje_final += (puntaje_inicial * ajuste_weapon[0]) / 100
    
    mod_ganancia = ajuste_perk[1] + ajuste_trait[1] + ajuste_weapon[1]

    mod_perdida = ajuste_perk[2] + ajuste_trait[2] + ajuste_weapon[2]

    return (puntaje_final,mod_ganancia,mod_perdida)

def check_stonk(stonk):
    """Obtener informacion sobre stonk"""
    
    pagina = requests.get(f"https://finance.yahoo.com/quote/{stonk}", headers=HEADERS)

    sopita = BeautifulSoup(pagina.text,features = 'lxml')
    
    banner = sopita.find('div',{'id':'quote-header-info'})

    valores = banner.find_all('span',{'class':'Trsdu(0.3s)'})

    return (banner.h1.text,valores[0].text,valores[1].text)

def actualizar_huachibonos(redditor_id,clase,item):
    """Actualizar los huachibonos comprados por el usuario"""

    costos = {"perk": 1000,"trait": 500, "weapon":250 }
    
    cantidad = costos[clase]

    #Acceder a la cuenta del cliente
    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:

        #Verificar que se tenga saldo suficiente para la transaccion
        if Huachis.saldo_total < cantidad:

            return random.choice(resp_tip_sinbineros)

        else:

            Huachis.Enviar_Bineros("Shop",cantidad,nota=item)

            Huachis.Update_Perks(clase,item)

            return random.choice(resp_huachibono)

def huachiswap(remitente,destinatario,ticker,cantidad):
    """DEX para intercambiar tokens, sin comisiones!"""

    if remitente in prohibido:
        return "wow :O chico listo"

    #Acceder a la HuachiNet
    Huachis = HuachiNet(remitente)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(remitente) == False:
        
        return random.choice(resp_tip_cuenta)

    shares = Huachis.Consultar_Shares()

    for share in shares:

        if ticker == share[0]:

            total = share[1]

            if total < cantidad:
                
                return f"Hijole wer@, no tienes suficientes {ticker} para completar la transaccion\n\nTienes {total:,} {ticker} en tu portafolio."

            else:

                stonk = check_stonk(ticker)

                Huachis.Enviar_Shares(destinatario,cantidad,ticker,stonk[1])

                return random.choice(resp_huachiswap)

    return "Ah caray! de esas no tiene! ¿Seguro que no se las robaron?"

def buy(redditor_id,ticker,cantidad):
    """PUMP IT"""

    if redditor_id in prohibido:
        return "wow :O chico listo"

    if ticker in stonks:

        #Acceder a la HuachiNet redditor
        Huachis_redditor = HuachiNet(redditor_id)

        #Primero verificar que el redditor tenga una cuenta
        if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
            return random.choice(resp_tip_cuenta)
    
        #Obtener informacion de la stonk
        stonk = check_stonk(ticker)

        #Calcular el costo total de la operacion: 1 huachis = 3 dolares
        costo_total = round((Decimal(stonk[1].replace(",","")) * cantidad) / 3)

        if costo_total > Huachis_redditor.saldo_total:

            return random.choice(resp_tip_sinbineros)
    
        else:

            Huachis_redditor.Enviar_Bineros("HuachiSwap",costo_total,nota=f"{ticker}")

            #Acceder a cuenta del broker
            Huachis_broker = HuachiNet("HuachiSwap")

            Huachis_broker.Enviar_Shares(redditor_id,cantidad,ticker,stonk[1].replace(",",""))

            return f"Compraste {cantidad:,} ({ticker}) a ${stonk[1]} por token\n\nMonto total de {costo_total * 3:,} usd ({costo_total:,} huachis UwU) retirados de tu cuenta\n\nPortafolio actualizado! Gracias por usar HuachiSwap ^_^" 

    else:

        return "Esa stonk no la tenemos en existencia, verifica que sea la correcta o que este listada en HuachiSwap 'UwU'"

def sell(redditor_id,ticker,cantidad):
    """DUMP IT"""

    if redditor_id in prohibido:
        return "wow :O chico listo"

    #Acceder a la HuachiNet redditor
    Huachis_redditor = HuachiNet(redditor_id)

    #Primero verificar que el redditor tenga una cuenta
    if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    #Obtener portafolio de redditor
    shares = Huachis_redditor.Consultar_Shares()

    for share in shares:

        #Verificar que tenga el activo a vender
        if ticker == share[0]:

            if int(share[1]) < cantidad:

                return f"Hijole wer@, no tienes suficientes {ticker} para completar la transaccion\n\nTienes {share[1]:,} ({ticker}) en tu portafolio."

            else:
                
                #Obtener informacion de la stonk
                stonk = check_stonk(ticker)

                #Vender shares!
                Huachis_redditor.Enviar_Shares("HuachiSwap",cantidad,ticker,stonk[1].replace(",",""))

                #Acceder a cuenta de broker

                Huachis_broker = HuachiNet("HuachiSwap")

                #Calcular dinero a enviar

                costo_total = round((cantidad * Decimal(stonk[1].replace(",",""))) / 3)

                Huachis_broker.Enviar_Bineros(redditor_id,costo_total,nota=f"{ticker}")

                return f"Vendiste {cantidad:,} ({ticker}) a ${stonk[1]} por token\n\nMonto total de {costo_total * 3:,} usd ({costo_total:,} huachis UwU) abonados a tu cuenta\n\nPortafolio actualizado! Gracias por usar HuachiSwap ^_^" 

    return "Ah caray! de esas no tiene! ¿Seguro que no se las robaron?"

def portafolio(redditor_id):
    """Huachifolio"""

    #Acceder a cuenta del redditor
    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el redditor tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    respuesta = f"Cartera de {redditor_id}:\n\nRecuerda: 1 huachis = 3 dolares!\n\nStonk (ticker) | Cantidad | Precio Promedio (usd) | Precio Actual (usd) | Valor Inicial (huachis) | Valor Actual (huachis)\n:--|:--:|:--:|:--:|--:|--:\n"

    shares = Huachis.Consultar_Shares()

    if shares != []:

        for share in shares:

            if share[1] > 1:

                stonk = check_stonk(share[0])

                valor_actual = round((share[1] * Decimal(stonk[1].replace(",",""))) / 3)

                valor_inicial = round((share[1] * Decimal(share[2])) / 3)

                respuesta += f"{share[0]} | {share[1]:,} | {share[2]:,} | {stonk[1]} | {valor_inicial:,} | {valor_actual:,} \n"

        return respuesta

    else:

        return "No tienes tokens! Lastima, usa HuachiSwap para comprar y vender tokens, no te quedes fuera de la diversion! :D"

def consultar_stonks():
    """Crear tabla de stonks disponibles en HuachiSwap"""

    respuesta = "HuachiSwap Liquidity Pool\n\nStonk (ticker) | Precio (usd) | Cambio 24 hrs\n:--|:--:|:--:\n"

    for ticker in stonks:

        stonk = check_stonk(ticker)

        respuesta += f"{stonk[0]} | {stonk[1]} | {stonk[2]}\n"

    return respuesta

if __name__ == "__main__":
    
    while True:

        start_time = time.time()

        resultado = empleado_del_mes()

        servicio_al_cliente()

        print("\nTermine mi trabajo patron!")

        print(f"--- {time.time() - start_time} seconds ---\nMovimientos: {resultado}")  

        time.sleep(30)
        
    
    
