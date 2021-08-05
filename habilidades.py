import math
import random
import re
import sqlite3
import time
from datetime import datetime
from core import HuachiNet
import traceback
import collections
import operator
import requests
from bs4 import BeautifulSoup
from decimal import *
import praw
import config
from misc import *

conn = sqlite3.connect("./boveda.sqlite3")

cursor = conn.cursor()

HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

reddit = praw.Reddit(client_id=config.APP_ID, 
                     client_secret=config.APP_SECRET,
                     user_agent=config.USER_AGENT, 
                     username=config.REDDIT_USERNAME,
                     password=config.REDDIT_PASSWORD) 

prohibido = ["Shop","HuachiSwap","Bodega","Huachicuenta"]

vib = ["MarcoCadenas","Empleado_del_mes","Disentibot","AutoModerator","UnidadVictimasEsp"]

stonks = shops['stonks']

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

    cursor = conn.cursor()

    cursor.execute(query,(comment_id,))

    conn.commit()

def saldazo(redditor_id) -> str:
    """Abierto todos los dias de 7am a 10pm"""

    if redditor_id in prohibido:
        return "wow :O chico listo"
    
    huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:
        return random.choice(resp_saldo) + f"\n\n{huachis.saldo_total:,} Huachis + {huachis.power} unidades de energia 🌀"

def tip(remitente,destinatario,cantidad) -> str:
    """Dar propina por publicaciones y comentarios"""

    if remitente in prohibido:
        return "wow :O chico listo"

    #Acceder a la HuachiNet
    huachis = HuachiNet(remitente)

    #Primero verificar que el remitente tenga una cuenta
    if huachis.Verificar_Usuario(remitente) == False:
        
        return random.choice(resp_tip_cuenta)

    else:
        #Verificar que se tenga saldo suficiente para la transaccion
        if huachis.saldo_total < cantidad:

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
                
                #Iniciamos transaccion
                huachis.Enviar_Bineros(destinatario,cantidad)

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

def rank(redditor_id, opcion) -> str:
    """Forbes Mujico - TOP Abinerados"""

    if redditor_id in prohibido:
        return "wow :O chico listo"

    #Acceder a la HuachiNet
    huachis = HuachiNet(redditor_id)

    #Primero verificar que el redditor tenga una cuenta
    if huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    ranking = huachis.Ranking()

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

def asalto(cholo,victima,tipo):
    """Saca bineros morro v4"""

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

        cholo_stats = tweak_stats(cholo)

        huachis_victima = HuachiNet(victima)

        victima_stats = tweak_stats(victima)

        #Primero verificar que la victima tenga una cuenta
        if huachis_victima.Verificar_Usuario(victima) == False:
        
            return "No tiene cuenta. Dime, que piensas robarle, ¿Los calzones?"

        if cholo in vib:

            num_cholo = 10000 + ( cholo_stats[0] + cholo_stats[2] ) - cholo_stats[1]

        else:
            
            num_cholo = random.randint(0,100) + ( cholo_stats[0] + cholo_stats[2] ) - victima_stats[1]

        num_victima = random.randint(0,100) + ( victima_stats[0] + victima_stats[2] ) - cholo_stats[1]

        if num_cholo > num_victima:

            if tipo == "asalto":

                cantidad_inicial = random.randint(50,500) 

            if tipo == "atraco":

                cantidad_inicial = round((int(huachis_victima.saldo_total) * random.randint(5,16)) / 100)

            if tipo == "levanton":

                cantidad_inicial = round((int(huachis_victima.saldo_total) * 16) / 100)

            ajuste = huachis_cholo.stats[3] - huachis_victima.stats[3] 

            cantidad_final = round( cantidad_inicial + ( (cantidad_inicial * ajuste ) / 100 ) )

            if huachis_victima.saldo_total == 0:

                return f"Le metiste una putiza totalmente gratis, no tiene dinero.\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            

            if cantidad_final <= 0:

                return f"Ganaste, pero el build del otro usuario absorbio tus ganancias. F\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
            elif cantidad_final > huachis_victima.saldo_total:

                #Enviar Binero
                huachis_victima.Enviar_Bineros(cholo,huachis_victima.saldo_total,nota=tipo.capitalize())

                return random.choice(resp_tumbar_cholo) + f"__{cholo} ganó toda la cartera de {victima} ({huachis_victima.saldo_total:,} huachis)__\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
            else:

                #Enviar Binero
                huachis_victima.Enviar_Bineros(cholo,cantidad_final,nota=tipo.capitalize())

                return random.choice(resp_tumbar_cholo) + f"\n\n__{cholo} ganó {cantidad_final:,} huachis (de la cartera de {victima})__\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
        elif num_victima > num_cholo:

            #Primero verificar que el cholo tenga una cuenta
            if huachis_cholo.Verificar_Usuario(cholo) == False:
        
                return "Perdiste, un momento, no tienes cuenta dentro del sistema. Y ahora que le voy a dar al otro usuario........"

            if tipo == "asalto":

                cantidad_inicial = random.randint(50,500) 

            if tipo == "atraco":

                cantidad_inicial = round((int(huachis_cholo.saldo_total) * random.randint(5,16)) / 100)

            if tipo == "levanton":

                cantidad_inicial = round((int(huachis_cholo.saldo_total) * 16) / 100)

            ajuste = huachis_victima.stats[3] - huachis_cholo.stats[3] 

            cantidad_final = round( cantidad_inicial + ( (cantidad_inicial * ajuste ) / 100 ) )

            if huachis_cholo.saldo_total == 0:

                return f"Perdiste, pero ve el lado positivo, no tienes dinero que darle\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
            
            if cantidad_final <= 0:

                return f"Perdiste, pero tu build absorbio tus los daños. Te salvaste morr@\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
            elif cantidad_final > huachis_cholo.saldo_total:

                #Enviar Binero
                huachis_cholo.Enviar_Bineros(victima,huachis_cholo.saldo_total,nota=tipo.capitalize())

                return random.choice(resp_tumbar_victima) + f"__{victima} ganó toda la cartera de {cholo} ({huachis_cholo.saldo_total:,} huachis)__\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
            else:

                #Enviar Binero
                huachis_cholo.Enviar_Bineros(victima,cantidad_final,nota=tipo.capitalize())

                return random.choice(resp_tumbar_victima) + f"\n\n__{victima} ganó {cantidad_final:,} huachis (de la cartera de {cholo})__\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"

        else:

            return "Empate tecnico. Baia, tantos calculos para que ninguno gane o pierda, chinguen a su madre los dos" 

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

        Huachis_shop.Enviar_Bineros(redditor_id,cantidad_ganada,nota="Premio Huachito")

        if comodin:
            
            mensaje = f">!{'   '.join(huachito)}!<\n\n>!Ganaste {cantidad_ganada:,} huachis ({numero_de_emojis_iguales} iguales usando comodin 🥓)!<"
        
        else:
            
            mensaje =  f">!{'   '.join(huachito)}!<\n\n>!Ganaste {cantidad_ganada:,} huachis ({numero_de_emojis_iguales} iguales)!<"
    
    else:
        
        mensaje = f">!{'   '.join(huachito)}!<\n\n>!{random.choice(respuestas_perdida)}!<"

    return mensaje

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

def check_stonk(stonk):
    """Obtener informacion sobre stonk"""
    
    pagina = requests.get(f"https://finance.yahoo.com/quote/{stonk}", headers=HEADERS)

    sopita = BeautifulSoup(pagina.text,features = 'lxml')
    
    banner = sopita.find('div',{'id':'quote-header-info'})

    valores = banner.find_all('span',{'class':'Trsdu(0.3s)'})

    return (banner.h1.text,valores[0].text,valores[1].text)

def actualizar_huachibonos(redditor_id,clase,item):
    """Actualizar los huachibonos comprados por el usuario"""

    costos = {"perk": 800,"trait": 400, "weapon":200 }
    
    cantidad = costos[clase]

    nalgoticas = ["LlamadoTuculo","VisionNalgotica","Conxuro",
                  "LecturaTarot","AguaCalzon","GagBall",
                  "Darketiza","EAHoe","Voodoo",
                  "BesoDraculona","OnlyFans","BotasPicos",
                  "DolorInfinito","Gothicc","TablaOuija"]

    otakos = ["Genkidama","ImpactTrueno","PolvoDiamante",
              "Rasegan","Omaewamushinderu","EsferaDragon",
              "PuertaMagica","PiedraEvolutiva","SemillaH",
              "TestoExodia","Dakimakura","MegaBuster",
              "CaparazonAzul","Sakabato","Shinigami"]

    guilds = {"AlianzaOtako": otakos,"DominioNalgoticas":nalgoticas}

    #Acceder a la cuenta del cliente
    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:

        seleccion = guilds[Huachis.guild]

        if item not in seleccion:

            return "Ese huachibono pertenece a otro gremio.\n\nPara conocer los huachibonos de tu clan usa el siguiente comando: !huachibono menu"

        #Verificar que se tenga saldo suficiente para la transaccion
        if Huachis.saldo_total < cantidad:

            return random.choice(resp_tip_sinbineros)

        else:

            Huachis.Enviar_Bineros("Shop",cantidad,nota=item)

            Huachis.Update_Perks(clase,item)

            return f"Enhorabuena!, haz comprado {item} al precio mas barato del mercado.\n\nWaporeon, te voy a regalar un pro-tip. Si quieres renovar tu build, solo unete de nuevo a tu gremio! (!guild <opcion>), recibes 3 huachibonos al azar por mil huachicoins.\nRegalado mi weromancer."

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

def unirse_guild(redditor_id,item):
    """Unirse a un gremio"""

    nalgoticas = [("LlamadoTuculo","VisionNalgotica","Conxuro",
                  "LecturaTarot","AguaCalzon"),
                  ("GagBall","Darketiza","EAHoe",
                  "Voodoo","BesoDraculona"),
                  ("OnlyFans","BotasPicos","DolorInfinito",
                  "Gothicc","TablaOuija")]

    otakos = [("Genkidama","ImpactTrueno","PolvoDiamante",
              "Rasegan","Omaewamushinderu"),
              ("EsferaDragon","PuertaMagica","PiedraEvolutiva",
              "SemillaHermitaño","TestoExodia"),
              ("Dakimakura","MegaBuster","CaparazonAzul",
              "Sakabato","Shinigami")]

    guilds = {"AlianzaOtako": otakos,"DominioNalgoticas":nalgoticas}

    cantidad = 1000

    #Acceder a la cuenta del cliente
    huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:

        #Verificar que se tenga saldo suficiente para la transaccion
        if huachis.saldo_total < cantidad:

            return random.choice(resp_tip_sinbineros)

        else:

            huachis.Enviar_Bineros("Shop",cantidad,nota=item)

            huachis.Update_Perks("guild",item)

            seleccion = guilds[item]

            perk = random.choice(seleccion[0])

            trait = random.choice(seleccion[1])

            weapon = random.choice(seleccion[2])

            huachis.Update_Perks("perk",perk)

            huachis.Update_Perks("trait",trait)

            huachis.Update_Perks("weapon",weapon)

            return f"Felicidades! Tu solicitud para unirte al gremio {item} ha sido aceptada.\n\nRecibe tu nuevo Build como bono de bienvenida\n\nPerk 🌀 : {perk} | Trait 🎭: {trait} | Weapon ⚔️: {weapon}"

def cambiar_flair(redditor_id,item):

    """Solo hacemos negocios"""

    cantidad = 5000

    #Acceder a la cuenta del cliente
    huachis_redditor = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:

        #Verificar que se tenga saldo suficiente para la transaccion
        if huachis_redditor.saldo_total < cantidad:

            return random.choice(resp_tip_sinbineros)

        else:

            huachis_redditor.Enviar_Bineros("Shop",cantidad,nota="Flair")

            start = item.index("!flair")

            texto = item[start:].replace("!flair","").strip()

            return f"{redditor_id}:{texto}"

def tweak_stats(redditor_id):

    """Calcular stats basales + cambios cuando los perks consumen energia"""

    huachis = HuachiNet(redditor_id)

    ultimate_stats = {"Genkidama" : (10,[0,0,(contar_miembros(huachis.guild)* 0.5),0]),
                 "LlamadoTuculo" : (10,[0,0,(contar_miembros(huachis.guild)* 0.5),0])}

    perks_stats = {"ImpactTrueno" : (5,[0,0,30,0]),
             "PolvoDiamante" : (5,[0,0,30,0]),
             "Rasegan" : (5,[0,0,50,0]),
             "Omaewamushinderu" : (5,[0,0,40,0]),
             "VisionNalgotica" : (5,[0,0,30,0]),
             "Conxuro" : (5,[0,0,30,20]),
             "LecturaTarot" : (5,[0,0,30,10]),
             "AguaCalzon" : (5,[0,0,40,0]),
             "Normal" : (0,[0,0,0,0])
             }

    base_stats = huachis.stats
    
    #Conocer perk del usuario
    if huachis.perk in ultimate_stats:

        mod_stats = ultimate_stats[huachis.perk]

    else:

        mod_stats = perks_stats[huachis.perk]

    #Si no tiene energia regresamos basestats
    if huachis.power < mod_stats[0]:

        return base_stats
    
    else:

        huachis.Consumir_Energia(mod_stats[0])

        new_stats = [ base_stats[i] + mod_stats[1][i] for i in range(4) ]

        return new_stats

def contar_miembros(guild):

    return cursor.execute("SELECT COUNT(usuario) FROM perks WHERE guild = ?",(guild,)).fetchone()[0]

def check_build(redditor_id):

    """Consultar build"""

    huachis = HuachiNet(redditor_id)

    stats = huachis.stats

    return f"Guild: {huachis.guild}\n\nBuild:\n🌀 {huachis.perk} | 🎭{huachis.trait} | ⚔️ {huachis.weapon}\n\nStats:\nAtk ⚔️{stats[0]} | Def 🛡️ {stats[1]} | Magia ✨ {stats[2]} | Dinero💰 {stats[3]}"