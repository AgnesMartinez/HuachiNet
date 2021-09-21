# This Python file uses the following encoding: utf-8
from datetime import datetime
import time
import sqlite3
import random
import string
import json
import re
import collections
import operator
from decimal import *
import praw
import config
import math
import traceback
import requests
from misc import *
from PIL import Image, ImageDraw, ImageFont
from base64 import b64encode

HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

reddit = praw.Reddit(client_id=config.APP_ID, 
                     client_secret=config.APP_SECRET,
                     user_agent=config.USER_AGENT, 
                     username=config.REDDIT_USERNAME,
                     password=config.REDDIT_PASSWORD) 


class HuachiNet():
    """Huachicol as a service
    ---------------------------------
    Requiere nombre de usuario para obtener la siguiente informacion:
    -Saldo total
    -Historial de movimientos (Global,Depositos,Retiros)

    El usuario puede realizar las siguientes funciones dentro de la red:
    
    -Bono_Bienvenida
    -Verificar_Usuario
    -Enviar_Bineros

    *Si el usuario no existe en la BD, se regresa None como valor
    """

    def __init__(self,usuario):
        #Conexion a BD
        self.conn = sqlite3.connect("boveda.sqlite3",check_same_thread=False)

        self.cursor = self.conn.cursor()

        self.id = usuario

        self.perk, self.power, self.trait, self.weapon, self.guild = self.Consultar_Perks()

        self.stats = self.Calcular_Stats()

        self.saldo_total = self.Consultar_Saldo()

        self.saldo_bancadenas = self.Consulta_Bancadenas()

        self.historial = self.Historial_Cuenta()

        self.depositos = self.Historial_Cuenta(tipo_movimiento="Deposito")

        self.retiros = self.Historial_Cuenta(tipo_movimiento="Retiro")

        self.asaltos = self.Historial_Cuenta(tipo_movimiento="Asalto")

        self.huachitos = self.Historial_Cuenta(tipo_movimiento="Huachito")

        self.premios_huachito = self.Historial_Cuenta(tipo_movimiento="Premio Huachito")

        self.atracos = self.Historial_Cuenta(tipo_movimiento="Atraco")

        self.levantones = self.Historial_Cuenta(tipo_movimiento="Levanton")

    def Verificar_Usuario(self,usuario):
        """Verificar si existe el cliente en la BD"""

        query = """SELECT ID FROM transacciones WHERE usuario=? LIMIT 1"""

        resultado = self.cursor.execute(query,(usuario,)).fetchone()

        if resultado == None:

            return False

        else:

            return True

    def Bono_Bienvenida(self,usuario):
        """Entregar bineros a los clientes nuevos"""

        if self.Verificar_Usuario(usuario) == False:

            query = """INSERT INTO transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

            timestamp = time.time()
        
            self.cursor.execute(query,(timestamp,usuario,1000,"Bono Inicial","Bodega"))

            self.cursor.execute(query,(timestamp,"Bodega",-1000,"Retiro",usuario))

            self.conn.commit()

            return True

        return False

    def Enviar_Bineros(self,usuario,cantidad,nota="Default"):
        """Registrar transacciones de bineros"""
        
        query = """INSERT INTO transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

        timestamp = time.time()
        
        if nota == "Default":

            self.cursor.execute(query,(timestamp,usuario,cantidad,"Deposito",self.id))

            negativo =  cantidad - (cantidad * 2)

            self.cursor.execute(query,(timestamp,self.id,negativo,"Retiro",usuario))

            self.conn.commit()

        elif nota != "Default":

            self.cursor.execute(query,(timestamp,usuario,cantidad,nota,self.id))

            negativo =  cantidad - (cantidad * 2)

            self.cursor.execute(query,(timestamp,self.id,negativo,nota,usuario))

            self.conn.commit()

    def Consultar_Saldo(self):
        """Consulta el saldo total del cliente"""

        query = """SELECT SUM(cantidad) FROM transacciones WHERE usuario=?"""

        self.cursor.execute(query,(self.id,))

        resultado = self.cursor.fetchone()

        return resultado[0]
        
    def Historial_Cuenta(self, tipo_movimiento = "Global"):
        """Consultar historial de movimientos del cliente desde el inicio de la cuenta"""
        
        if tipo_movimiento == "Global":

            query = """SELECT id,timestamp,cantidad,nota,origen_destino FROM transacciones WHERE usuario=? ORDER BY id DESC"""
            
            parametros = (self.id,)

        else:
                
            query = """SELECT id,timestamp,cantidad,origen_destino FROM transacciones WHERE usuario=? AND nota=? ORDER BY id DESC"""
                
            parametros = (self.id,tipo_movimiento)

        return self.cursor.execute(query,parametros).fetchall()
                    
    def Mujicanos(self):
        """Lista de usuarios activos"""

        #Obtener lista de usuarios
        query = """SELECT usuario FROM transacciones WHERE nota='Bono Inicial'"""

        self.cursor.row_factory = lambda cursor, row: row[0]

        resultado = self.cursor.execute(query).fetchall()

        return list(filter(None,resultado))

    def Ranking(self):
        """Forbes Mujico - Usuarios Abinerados"""

        #Obtener lista de usuarios
        query = """SELECT usuario, SUM(cantidad) as cantidad FROM transacciones WHERE usuario in (SELECT usuario FROM transacciones WHERE nota='Bono Inicial') GROUP BY usuario ORDER BY cantidad DESC"""
        
        return self.cursor.execute(query).fetchall()

    def Huachiclave(self):
        """Regresa la huachiclave vigente o genera una nueva"""

        query = """SELECT timestamp,huachiclave,cantidad,entregado FROM huachilate WHERE entregado = '0' ORDER BY timestamp"""

        query2 = """INSERT INTO huachilate (timestamp,huachiclave,cantidad,entregado) VALUES (?,?,?,?)"""

        resultado = self.cursor.execute(query).fetchall()

        if resultado == []:
            
            timestamp = time.time()
            
            huachiclave = "".join(random.choices(string.ascii_letters + string.digits,k = 7))

            cantidad = random.randint(5000,50000)

            self.cursor.execute(query2,(timestamp,huachiclave,cantidad,0))

            self.conn.commit()

            return (timestamp,huachiclave,cantidad)
        
        else:
            return resultado[-1]

    def Consultar_Perks(self):
        """Consultar perk, power, trait , arma y guild"""

        query = """SELECT perk,power,trait,weapon,guild FROM perks WHERE usuario = ?"""

        resultado = self.cursor.execute(query,(self.id,)).fetchall()

        #En caso de que el usuario no este en la tabla de perks, se añadira con stats basicos.
        if resultado == []:

            timestamp = time.time()
            
            query2 = """INSERT INTO perks (timestamp,usuario,perk,power,trait,weapon,guild) VALUES (?,?,?,?,?,?,?)"""

            self.cursor.execute(query2,(timestamp,self.id,"Normal",100,"Normal","Navaja","Normal"))

            self.conn.commit()

            return ("Normal",100,"Normal","Navaja","Normal")

        else:

            return resultado[-1]

    def Update_Perks(self,clase,item):
        """Agregar y modificar perk,trait, weapon y guild de los mujicanos"""

        query = f"""UPDATE perks SET {clase} = ? WHERE usuario = ?"""

        query2 = """UPDATE perks SET power = 100 WHERE usuario = ?"""

        self.cursor.execute(query,(item,self.id))

        if clase == "perk":

            self.cursor.execute(query2,(self.id,))

        self.conn.commit()

    def Consumir_Energia(self,cantidad):
        """Los perks necesitan energia para funcionar"""

        energia = self.power - cantidad

        query = """UPDATE perks SET power = ? WHERE usuario = ?"""

        self.cursor.execute(query,(energia,self.id))

        self.conn.commit()

    def Calcular_Stats(self):
        """NRPG - Niño Rata Playing Game"""

        baseStats = {"ConductoresNocturnos" : [60,50,40,40],
                     "AlianzaOtako" : [30,60,40,60],
                     "DominioNalgoticas" : [60,30,60,40],
                     "Corvidos" : [40,60,40,60],
                     "Normal" : [50,50,50,50],
                     "ElForastero" : [50,50,50,50]}

        perkStats = json.loads(open("./assets/perks.json","r",encoding="utf-8").read())

        traitStats = json.loads(open("./assets/traits.json","r",encoding="utf-8").read())

        weaponStats = json.loads(open("./assets/weapons.json","r",encoding="utf-8").read())

        #Stats base + perks stats
        base = baseStats[self.guild]

        perk = perkStats[self.perk]

        trait = traitStats[self.trait]

        weapon = weaponStats[self.weapon]

        return [ base[i] + perk[i] + trait[i] + weapon[i] for i in range(4) ]
    
    def Consulta_Bancadenas(self):

        """Consulta saldo en Bancadenas"""

        query = "SELECT SUM(cantidad) FROM bancadenas WHERE usuario = ?"

        return self.cursor.execute(query,(self.id,)).fetchone()[0]

    def Registro_Bancadenas(self,cantidad,nota):

        """Registrar movimientos de cuenta en Bancadenas"""

        query = "INSERT INTO bancadenas (timestamp,usuario,cantidad,nota) VALUES (?,?,?,?)"

        timestamp = time.time()

        self.cursor.execute(query,(timestamp,self.id,cantidad,nota))

        self.conn.commit()



def saldazo(redditor_id) -> str:
    """Abierto todos los dias de 7am a 10pm"""

    if redditor_id in prohibido:
        return "wow :O chico listo"
    
    huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:
        return random.choice(resp_saldo) + f"\n\nCartera Principal: {huachis.saldo_total:,} huachis + {huachis.power} unidades de energia 🌀\n\nCuenta Bancadenas: {huachis.saldo_bancadenas} huachis"

def tip(remitente,destinatario,cantidad) -> tuple:
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
            cuenta_dias = 30 if destinatario == 'Empleado_del_mes' else edad_cuenta(destinatario)

            if cuenta_dias < 28:

                return (False,"El usuario al que quieres enviar no tiene la madurez suficiente para entrar al sistema, es un pinche mocoso miado, dejalo ahi.")

            else:
                
                #Iniciamos transaccion

                cuenta_nueva = huachis.Bono_Bienvenida(destinatario)

                huachis.Enviar_Bineros(destinatario,cantidad)

                if destinatario == "Empleado_del_mes":

                    return (cuenta_nueva,random.choice(resp_tip_empleado) + f" [{cantidad} Huachicoin(s) Enviado(s)]")

                elif remitente == "Empleado_del_mes" and destinatario == "Empleado_del_mes":

                    return (cuenta_nueva,"autotip")

                else:
                
                    return (cuenta_nueva,random.choice(resp_tip_envio) + f" [{cantidad} Huachicoin(s) Enviado(s)]")

def edad_cuenta(redditor_id) -> int:
    """calcular la edad en dias de la cuenta"""

    diff = datetime.utcnow() - datetime.fromtimestamp(reddit.redditor(redditor_id).created_utc)

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

                return  f"{random.choice(resp_tumbar_cholo)}\n\n__{cholo} ganó toda la cartera de {victima} ({huachis_victima.saldo_total:,} huachis)__\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
            else:

                #Enviar Binero
                huachis_victima.Enviar_Bineros(cholo,cantidad_final,nota=tipo.capitalize())

                return  f"{random.choice(resp_tumbar_cholo)}\n\n__{cholo} ganó {cantidad_final:,} huachis (de la cartera de {victima})__\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
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

                return f"Perdiste, pero tu build absorbio los daños. Te salvaste morr@\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
            elif cantidad_final > huachis_cholo.saldo_total:

                #Enviar Binero
                huachis_cholo.Enviar_Bineros(victima,huachis_cholo.saldo_total,nota=tipo.capitalize())

                return f"{random.choice(resp_tumbar_victima)}\n\n__{victima} ganó toda la cartera de {cholo} ({huachis_cholo.saldo_total:,} huachis)__\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"
            
            else:

                #Enviar Binero
                huachis_cholo.Enviar_Bineros(victima,cantidad_final,nota=tipo.capitalize())

                return f"{random.choice(resp_tumbar_victima)}\n\n__{victima} ganó {cantidad_final:,} huachis (de la cartera de {cholo})__\n\nGuild | Mujicano | 🌀 | 🎭 | ⚔️\n:--|:--|:--:|:--:|:--:\n{huachis_cholo.guild} | {cholo} | {huachis_cholo.perk} | {huachis_cholo.trait} | {huachis_cholo.weapon}\n{huachis_victima.guild} | {victima} | {huachis_victima.perk} | {huachis_victima.trait} | {huachis_victima.weapon}"

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

            elif regalo == 'doujin':

                doujin = random.choice(doujins)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado hentai, Yamete kudasai!\n\n [Abrir Regalo]({doujin})")

                return random.choice(resp_shop)

            elif regalo == 'viejo' or regalo == 'paella' :

                viejo = random.choice(viejos)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado un viejo sabrozo, cuidoado porque salpica \n\n [Abrir Regalo]({viejo})")

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

def pokermujicano(remitente,destinatario):

    if remitente in prohibido:
        return "wow :O chico listo"

    if remitente == destinatario:

        return "Con que quieres jugar solitario ;) coshino"

    #Acceder a cuenta de redditors
    Huachis_remitente = HuachiNet(remitente)

    Huachis_destinatario = HuachiNet(destinatario)
        
    #Verificar que ambos tengan cuenta
    if Huachis_remitente.Verificar_Usuario(remitente) == False:
        
        return random.choice(resp_tip_cuenta)

    elif Huachis_destinatario.Verificar_Usuario(destinatario) == False:
        
        return "Tu oponente no tiene cuenta, dale una propina para que pueda jugar"

    else: 
        #Verificar que ambos tengan saldo
        if Huachis_remitente.saldo_total < 300:
            
            return random.choice(resp_tip_sinbineros)

        elif Huachis_destinatario.saldo_total < 300:
            
            return "Tu oponente no tiene suficiente dinero para participar en el juego"

        else:
            
            #Cobrar la entrada
            cantidad = random.randint(20,300)
            
            Huachis_remitente.Enviar_Bineros("Shop",cantidad,nota="Poker")

            Huachis_destinatario.Enviar_Bineros("Shop",cantidad,nota="Poker")
            
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

    mano_remitente = manos[0:5]

    mano_destinatario = manos[5:10]

    casa = combinaciones_poker(mano_remitente)

    redditor = combinaciones_poker(mano_destinatario)

    cartas_r = f'{mano_remitente[0][0]} : {mano_remitente[0][1]} | {mano_remitente[1][0]} : {mano_remitente[1][1]} | {mano_remitente[2][0]} : {mano_remitente[2][1]} | {mano_remitente[3][0]} : {mano_remitente[3][1]} | {mano_remitente[4][0]} : {manos[4][1]}'

    cartas_d = f'{mano_destinatario[0][0]} : {mano_destinatario[0][1]} | {mano_destinatario[1][0]} : {mano_destinatario[1][1]} | {mano_destinatario[2][0]} : {mano_destinatario[2][1]} | {mano_destinatario[3][0]} : {mano_destinatario[3][1]} | {mano_destinatario[4][0]} : {mano_destinatario[4][1]}'


    #Victoria: Remitente
    if casa[0][1] > redditor[0][1]:

        #Acceder a la cuenta de la shop
        Huachis_shop = HuachiNet("Shop")

        Huachis_shop.Enviar_Bineros(remitente,pot,nota="Poker")

        return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {remitente}, mano con {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

    #Victoria: Destinatario
    elif casa[0][1] < redditor[0][1]:

        #Acceder a la cuenta de la shop
        Huachis_shop = HuachiNet("Shop")

        Huachis_shop.Enviar_Bineros(destinatario,pot,nota="Poker")
        
        return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {destinatario}, mano con {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

    #Empate tecnico, desempate segun combinacion (4 escenarios)
    elif casa[0][1] == redditor[0][1]:

        letras = {"K":13,"A":14,"J":11,"Q":12}

        if casa[2] in palos or redditor[2] in palos:
            #Escenario 1 - Palo que provoco escalera color, color
            carta_alta_casa = [carta[1] for carta in mano_remitente if carta[2] == casa[2]]
        
            carta_alta_redditor = [carta[1] for carta in mano_destinatario if carta[2] == redditor[2]]

            if carta_alta_casa[0].isdigit() == False:

                carta_alta_casa = [valor for letra,valor in letras.items() if letra == carta_alta_casa[0]]

            if carta_alta_redditor[0].isdigit() == False:

                carta_alta_redditor = [valor for letra,valor in letras.items() if letra == carta_alta_redditor[0]]

            if int(carta_alta_casa[0]) > int(carta_alta_redditor[0]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(remitente,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {remitente}, mano con {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

            elif int(carta_alta_casa[0]) < int(carta_alta_redditor[0]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(destinatario,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {destinatario}, mano con {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

            elif int(carta_alta_casa[0]) == int(carta_alta_redditor[0]):

                return f"_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nEmpate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste\n\n_Pot: {pot} huachicoins_"
        
        #Escenario 2 - ambas manos tienen digito como carta alta
        elif casa[2].isdigit() and redditor[2].isdigit():
            
            if int(casa[2]) > int(redditor[2]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(remitente,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {remitente}, mano con {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

            elif int(casa[2]) < int(redditor[2]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(destinatario,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {destinatario}, mano con {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

            elif int(casa[2]) == int(redditor[2]):

                return f"_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nEmpate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste\n\n_Pot: {pot} huachicoins_"
        
        #Escenario 3 -Ambas manos tiene carta alta
        elif casa[2] == "None" and redditor[2] == "None": 
            #El valor de la carta mas alta
            if max(casa[1]) > max(redditor[1]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(remitente,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {remitente}, mano con {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

            elif max(casa[1]) < max(redditor[1]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(destinatario,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {destinatario}, mano con {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

            elif max(casa[1]) == max(redditor[1]):

                return f"_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nEmpate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste\n\n_Pot: {pot} huachicoins_"        

        #Escenario 4 - Una mano tiene digito como carta alta, la otra tiene letra
        else:

            carta_alta_casa = casa[2]

            carta_alta_redditor = redditor[2]

            if carta_alta_casa[0].isdigit() == False and carta_alta_casa != "None":

                carta_alta_casa = [valor for letra,valor in letras.items() if letra == carta_alta_casa[0]]

            if carta_alta_redditor[0].isdigit() == False and carta_alta_redditor != "None":

                carta_alta_redditor = [valor for letra,valor in letras.items() if letra == carta_alta_redditor[0]]

            if int(carta_alta_casa[0]) > int(carta_alta_redditor[0]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(remitente,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {remitente}, mano con {casa[0][0]}\n\n_Pot: {pot} huachicoins_' 

            elif int(carta_alta_casa[0]) < int(carta_alta_redditor[0]):

                #Acceder a la cuenta de la shop
                Huachis_shop = HuachiNet("Shop")

                Huachis_shop.Enviar_Bineros(destinatario,pot,nota="Poker")

                return f'_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nVictoria para {destinatario}, mano con {redditor[0][0]}\n\n_Pot: {pot} huachicoins_'

            elif int(carta_alta_casa[0]) == int(carta_alta_redditor[0]):

                return f"_Poker Estilo Mujico_\n\nMano de {remitente}\n\n{cartas_r}\n\nMano de {destinatario}\n\n{cartas_d}\n\nEmpate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste\n\n_Pot: {pot} huachicoins_"
                
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
                puntaje = ("Escalera real de color",10)

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
                    puntaje = ("Escalera de color",9)

                    return (puntaje,valores_corregidos,palo)
                
                else:
                    #Puntaje Color
                    puntaje = ("Color",6)

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
        puntaje = ("Escalera Alta",5)

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
            puntaje = ("Escalera",5)

            return (puntaje,valores_corregidos,"None")

    #Poker / Tercia / Dos pares / Pares
    pares = 0
    valor_varios = ""
    for valor in valores:
        if valores_cartas.count(valor) ==  4:
            #Poker
            puntaje = ("Poker",8)
            valor_varios = valor

            return (puntaje,valores_corregidos,valor_varios)

        if valores_cartas.count(valor) ==  3:
            #Tercia
            puntaje = ("Tercia",4)
            valor_varios = valor

            return (puntaje,valores_corregidos, valor_varios)

        if valores_cartas.count(valor) ==  2:
            #Sumar par
            pares += 1
            valor_varios = valor

    if pares == 2:
        #Puntaje dos pares
        puntaje = ("Dos Pares",3)

        return (puntaje,valores_corregidos, valor_varios)
    
    elif pares == 1:
        #Puntaje pares
        puntaje = ("Par",2)
        
        return (puntaje,valores_corregidos,valor_varios)
    
    puntaje = ("Carta alta",1)

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
            
            Huachis_redditor.cursor.execute("""INSERT INTO boletitos (timestamp,usuario,huachiclave) VALUES (?,?,?)""",valores)

            Huachis_redditor.conn.commit()

            huachicuenta = HuachiNet("Huachicuenta")

            if huachicuenta.saldo_total >= huachiclave[2]:
                premio_huachilate()

            return random.choice(resp_huachilate)

def premio_huachilate():
    """Repartir premios del huachilate"""

    huachicuenta = HuachiNet("Huachicuenta")

    huachiclave = huachicuenta.Huachiclave()

    participantes = [usuario[0] for usuario in huachicuenta.cursor.execute("""SELECT usuario FROM boletitos WHERE huachiclave = ?""",(huachiclave[1],)).fetchall()]

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

    selftext = f"Los ganadores de este Huachilote, con fecha y hora de {fecha_huachilote}　 　　　　　　　　　　 ✦ 　　　　   　 　　　˚　　　　　　　　　　　　　　*　　　　　　   　　　　　　　　　　　　　　　.　　　　　　　　　　　　　　. 　　      💫 　　　　　　　 ✦              🌝  　　　　 　　　　　 🌠 　                                               \n\n👻  ,　　   　.　　　　　　　　　　　　　.　　　ﾟ　  　　　.　　　　　　　　　　　　　.   ,　　　　　　.　　　　　　 ☀                                                🌞  　　　　　           ☄        . 　　　　　　　　　　.　　　　　　　　　      👽　　      　　. 　　　　　　,　　  　　　　.　　　　　　 ☀                                  　 ☄ 　　　    　　✦\n\n    1er | {ganadores[0]} | {premios[0]:,} huachis\n\n✦ 　   　　　,　　　　　　　　　🚀 　　　　 　　,　　　 ‍ ‍ ‍ ‍ 　　　　🌠 　　　　　　　　　　　 　 　　　　　　　　　　　˚　　　 　   　　　　,　　    　　　　　　　.　　　                  🛰  　　    　　 　　　　　.　　　　　　　　　　　　.　　　　　　　　　　　　　　　* 　　   　　　　　 ✦ 　　　　　　　  　\n\n🌟 　　 　　　　　　　 　　　　　.　　　　　　　　　　　　　　　　　　.　　　　　    　　. 　 　　　　　.　　　　  🌚                                                             🌠  　　　　　   　　　　　.　　　　　　　　　　　.　　　　　　　　　　   　 ˚　　　          \n\n👽 　　　　ﾟ　　　　　.　　　                             　　                      🛸 　　　　　　　　　　. 　　 　                            🌎 ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍             ,　 　　　　　            　　*.　　　　　 　　　　.　　　　　　　　　　 ✦ 　　　˚　　　　　　*　👾\n\n    2do | {ganadores[1]} | {premios[1]:,} huachis\n\n. 　. .　　　　　　　　　　 ✦ 　　　　   　 　　　 🛰˚　　　　　　　　　　　　　　*　　　　　　　　　　　　.　　　　　　　　　　　　. 　　 　　　 🌟 　                                   \n\n👾                               ✦ 　　　                         　　 🌠 　　　　　 　 ‍ ‍ ‍ ‍　 　　 ☄ 　　　　　　　　　　,　　   　 　　　　,　　    　　　　　　　　　.　　　  　　    　　　　　 　　　　　.　　　　　　　　　　　　　.　　　　　　　　　　　　　　　* ✦ 　　　　　　　         　        　 👽 　　　 　　 　                     　\n\n ☄ 　　　　　 　　　　　.　　　　　　　　　　　　　　　.　　　　　　　　　　　　　.　　　ﾟ　  　　　.　　　 🛸 　　　　　　　　　 　. ,　　　　　　　.　　　　　　    　　　　🌞 　　　　　　　 　. ☄\n\n    3er | {ganadores[2]} | {premios[2]:,} huachis\n\n✦ 　   　　　,　　　　　　　　　　　              🚀 　　　　 　　,　　　 ‍ ‍ ‍ ‍ 　                     \n\n🌌.　　　　　 　　                              🌟 　　　.　　　　　　　　　　　　　 　　　　　　　　　　　　　˚　　   　　                                  　　,　　　　　 🌝 　　　       　   　                 　　　 🛸 　　　　.　　 　                           \n\n🛰  　　    　　　　　 　　　　　.　　　　　　　　　　　　　.　　　　 👾　　　　　　　　　* 　　   　　　 　　 ✦ 　　　　　　　         　    🌟 .　　　　　　　　　　　　　　　　　　.　　                   🦜 　　. 　 　　                            　.　　　　 \n\n🌚 .　　　　　　　　　　　.　　　　　　　 👽 　　　                                          　🌜ﾟ　　　　　.　　　　　　　　　　　　　　　. 　　 　\n\n🌎 ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ,　 　　　　　　　　　　　　 　　*.　　　　　 　　　　　　　　　　　　　　.　　　　　　　　　　 ✦ 　　　　   　                Felicidades a los ganadores del huachilote　 🛸 　　　　　　　　　　　.　　　　　　　　　."

    subs = ["Mujico","TechoNegro","memexico"]
    # huachinews flair_id='a0a7193c-579b-11eb-8162-0e6a96a0cacd'
    for sub in subs:

        if sub == "Mujico":

            reddit.subreddit(sub).submit(f'Ganadores del Huachilate serie: "{huachiclave[1]}" :D', selftext=selftext, flair_id='a0a7193c-579b-11eb-8162-0e6a96a0cacd')

        else: 

            reddit.subreddit(sub).submit(f'Ganadores del Huachilate serie: "{huachiclave[1]}" :D', selftext=selftext)

    #Actualizar columna entregado para que se genere nueva huachiclave
    huachicuenta.cursor.execute("""UPDATE huachilate SET entregado = 1 WHERE huachiclave = ?""",(huachiclave[1],))

    huachicuenta.conn.commit()

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

    conductores = ["BendicionRaquel","CeroMiedo","CampeonAjedrez",
              "MonaInflable","MALVERDE","SemenArdiente",
              "Proxeneta","AngelesCharlie","Chambeadoras",
              "KingoftheRoad","Stiletto","BrazoTrailero",
              "MenageaTrapo","PastillaAzul","DragonDrilldo"]

    corvidos = ["ExorcismoFantasmas","ParvadaCuervos","SaposAlucinogenos","Trepanacion","Sangria",
              "BitcoinMedieval","Sapo","MascaraMDLP","BibliaLuisXIV","HierbasAromaticas",
              "SanguijuelaGoliat","PaloMedico","JeringaCocaina","SerruchoOxidado","Flammenwerfer"]

    guilds = {"AlianzaOtako": otakos,"DominioNalgoticas":nalgoticas,
              "ConductoresNocturnos" : conductores, "Corvidos": corvidos}

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

            return f"Enhorabuena!, haz comprado {item} al precio mas barato del mercado.\n\nWaporeon, Si quieres renovar tu build, solo unete de nuevo a tu gremio! (!guild <opcion>), recibes 3 huachibonos al azar por mil huachicoins."

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

    conductores = [("BendicionRaquel","CeroMiedo","CampeonAjedrez",
              "MonaInflable","MALVERDE"),("SemenArdiente",
              "Proxeneta","AngelesCharlie","Chambeadoras",
              "KingoftheRoad"),("Stiletto","BrazoTrailero",
              "MenageaTrapo","PastillaAzul","DragonDrilldo")]

    corvidos = [("ExorcismoFantasmas","ParvadaCuervos","SaposAlucinogenos","Trepanacion","Sangria"),
              ("BitcoinMedieval","Sapo","MascaraMDLP","BibliaLuisXIV","HierbasAromaticas"),
              ("SanguijuelaGoliat","PaloMedico","JeringaCocaina","SerruchoOxidado","Flammenwerfer")]

    guilds = {"AlianzaOtako": otakos,"DominioNalgoticas":nalgoticas,
              "ConductoresNocturnos": conductores, "Corvidos": corvidos}

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

            return f"{redditor_id}::{texto}"

def tweak_stats(redditor_id):

    """Calcular stats basales + cambios cuando los perks consumen energia"""

    huachis = HuachiNet(redditor_id)

    ultimate_stats = {"Genkidama" : (10,[0,0,(contar_miembros(huachis.guild)* 0.5),0]),
                 "LlamadoTuculo" : (10,[0,0,(contar_miembros(huachis.guild)* 0.5),0]),
                 "BendicionRaquel" : (10,[0,0,0,(contar_miembros(huachis.guild)* 0.5)]),
                 "ExorcismoFantasmas" : (10,[0,0,50 + (contar_miembros(huachis.guild)* 0.5),0])
                 }

    perks_stats = {"ImpactTrueno" : (5,[0,0,30,0]),
             "PolvoDiamante" : (5,[0,0,30,0]),
             "Rasegan" : (5,[0,0,50,0]),
             "Omaewamushinderu" : (5,[0,0,40,0]),
             "VisionNalgotica" : (5,[0,0,30,0]),
             "Conxuro" : (5,[0,0,30,20]),
             "LecturaTarot" : (5,[0,0,30,10]),
             "AguaCalzon" : (5,[0,0,40,0]),
             "Normal" : (0,[0,0,0,0]),
             "CeroMiedo" : (5,[0,-30,20,0]),
             "CampeonAjedrez" : (5,[0,0,30,0]),
             "MonaInflable" : (5,[0,30,0,0]),
             "MALVERDE" : (5,[0,0,30,0]),
             "ParvadaCuervos" : (5,[0,0,30,0]),
             "SaposAlucinogenos" : (5,[0,0,40,0]),
             "Trepanacion" : (5,[0,0,20,0]),
             "Sangria" : (5,[0,0,10,0]),
             "Gabardina" : (0,[0,0,0,0])
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

    huachis = HuachiNet("Empleado_del_mes")
    
    return huachis.cursor.execute("SELECT COUNT(usuario) FROM perks WHERE guild = ?",(guild,)).fetchone()[0]

def check_build(redditor_id):

    """Consultar build"""

    huachis = HuachiNet(redditor_id)

    stats = huachis.stats

    return f"Guild: {huachis.guild}\n\nBuild:\n🌀 {huachis.perk} | 🎭{huachis.trait} | ⚔️ {huachis.weapon}\n\nStats:\nAtk ⚔️{stats[0]} | Def 🛡️ {stats[1]} | Magia ✨ {stats[2]} | Dinero💰 {stats[3]}"

def deposito_bancadenas(redditor_id,cantidad):
    """Depositar churupos en bancadenas"""

    #Acceder a cuenta del cliente

    huachis = HuachiNet(redditor_id)

    #Verificar que tenga cuenta en la HuachiNet
    if huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    if huachis.saldo_total < cantidad:

        return random.choice(resp_tip_sinbineros)

    else:

        #PROTECCION cuando no se tiene cuenta en Bancadenas
        if huachis.saldo_bancadenas == None:

            saldo_bancadenas = 0

        else:

            saldo_bancadenas = huachis.saldo_bancadenas

        #Limite de cuenta == 30,000 huachis
        limite_cuenta = 50000

        if saldo_bancadenas >= limite_cuenta:

            return "No puedes depositar mas huachis, saldo maximo de 30,000 huachis por cuenta (┛◉Д◉)┛彡┻━┻ "

        excedente = saldo_bancadenas + cantidad 

        if  excedente > limite_cuenta:

            total = limite_cuenta - saldo_bancadenas

        else:

            total = cantidad

        #Mover huachis de main wallet a bancadenas
        huachis.Enviar_Bineros("Bancadenas",total)

        #Registrar transaccion en ledger bancadenas

        huachis.Registro_Bancadenas(total,"Deposito")

        return f"La cantidad de {total:,} huachis han sido abonadas a su cuenta\n\nSu Saldo actual es de: {huachis.Consulta_Bancadenas():,} huachicoin(s)\n\nGracias por usar Bancadenas! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧"

def retiro_bancadenas(redditor_id,cantidad):

    """Retirar churupos de bancadenas"""

    #Acceder a cuenta del cliente
    huachis_redditor = HuachiNet(redditor_id)

    #Verificar que tenga cuenta en la HuachiNet
    if huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:

        if huachis_redditor.saldo_bancadenas == None:

            return "Su cuenta en Bancadenas esta llena de lagrimas chairas ಥ_ಥ ..........no tienen valor comercial, deposite algo a su cuenta oiga."

        if huachis_redditor.saldo_bancadenas < cantidad:

            return f"No es posible completar la transferencia, el saldo de su cuenta es insuficiente o(╥﹏╥)o\n\nSu saldo actual es de: {huachis_redditor.saldo_bancadenas:,} huachicoin(s)"

        
        huachis_bancadenas = HuachiNet("Bancadenas")

        #Mover huachis de bancadenas a main wallet
        huachis_bancadenas.Enviar_Bineros(redditor_id,cantidad)

        #Registrar transaccion en ledger bancadenas
        huachis_redditor.Registro_Bancadenas(-cantidad,"Retiro")

        return f"La cantidad de {abs(cantidad):,} huachis han sido retiradas de su cuenta\n\nSu saldo actual es de: {huachis_redditor.Consulta_Bancadenas():,} huachicoin(s)\n\nGracias por usar Bancadenas! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧"

def generar_im_dinero(faiter1,faiter2,tipo):
 
    cholo = HuachiNet(faiter1)

    victima = HuachiNet(faiter2)

    data = cholo.cursor.execute("SELECT * FROM transacciones WHERE usuario = ? AND nota = ? ORDER BY timestamp DESC ",(faiter1,tipo.capitalize())).fetchone()

    img = Image.new('RGB', (800, 600), color = (38, 50, 56))
 
    d = ImageDraw.Draw(img)

    fnt = ImageFont.truetype("./assets/Symbola.ttf", 28, encoding='unic')

    if data[3] > 0:

        ganador = faiter1
    
    else:

        ganador = faiter2

    d.text((50,50), f"👾 Mujico RPG  👾 |  ID: {data[0]}\n\n{faiter1}    Guild    {cholo.guild}\nBuild    ( ⚔ {cholo.stats[0]} | 🛡 {cholo.stats[1]} | ✨ {cholo.stats[2]} | 💰 {cholo.stats[3]} )\n    🌀 {cholo.perk}\n    🎭 {cholo.trait}\n    ⚔ {cholo.weapon}\n---------------------------------------------------------\n\n{faiter2}    Guild    {victima.guild}\nBuild    ( ⚔ {victima.stats[0]} | 🛡 {victima.stats[1]} | ✨ {victima.stats[2]} | 💰 {victima.stats[3]} )\n    🌀 {victima.perk}\n    🎭 {victima.trait}\n    ⚔ {victima.weapon}\n---------------------------------------------------------\n\nGanador: {ganador} ({abs(data[3]):,} huachis)\n    ┬┴┬┴┤( ͡° ͜ʖ├┬┴┬┴", fill=(255,196,0), font=fnt,spacing=5)
 
    img.save('./assets/logos/robo.png')

def generar_im_sin(faiter1,faiter2,won):
 
    cholo = HuachiNet(faiter1)

    victima = HuachiNet(faiter2)

    img = Image.new('RGB', (800, 600), color = (38, 50, 56))
 
    d = ImageDraw.Draw(img)

    fnt = ImageFont.truetype("./assets/Symbola.ttf", 28, encoding='unic')

    if won == 1:

        ganador = faiter1
    
    else:

        ganador = faiter2

    d.text((50,50), f"👾 Mujico RPG  👾\n\n{faiter1}    Guild    {cholo.guild}\nBuild    ( ⚔ {cholo.stats[0]} | 🛡 {cholo.stats[1]} | ✨ {cholo.stats[2]} | 💰 {cholo.stats[3]} )\n    🌀 {cholo.perk}\n    🎭 {cholo.trait}\n    ⚔ {cholo.weapon}\n---------------------------------------------------------\n\n{faiter2}    Guild    {victima.guild}\nBuild    ( ⚔ {victima.stats[0]} | 🛡 {victima.stats[1]} | ✨ {victima.stats[2]} | 💰 {victima.stats[3]} )\n    🌀 {victima.perk}\n    🎭 {victima.trait}\n    ⚔ {victima.weapon}\n---------------------------------------------------------\nGanador: {ganador}\n    ┬┴┬┴┤( ͡° ͜ʖ├┬┴┬┴", fill=(255,196,0), font=fnt,spacing=5)
 
    img.save('./assets/logos/robo.png')

def upload_imgur():

    headers = {"Authorization": f"Client-ID {config.IM_CLIENT_ID}"}

    api_key = config.IM_CLIENT_SECRET

    url = "https://api.imgur.com/3/upload.json"

    name = random.choices(string.ascii_letters + string.digits,k = 7)

    data = {
        'key': api_key, 
        'image': b64encode(open('./assets/logos/robo.png', 'rb').read()),
        'type': 'base64',
        'name': f'{name}',
        'title': f'Atracos {name}'
        }

    response = requests.post(url,headers=headers,data=data)

    if response.status_code == 200:

        url = response.json()["data"]["link"]

    else:

        url = ""

    return (response.status_code,url)

    
class Empleado_del_mes():

    """Cirilo por fin fue a la preparatoria :')"""

    def __init__(self):

        self.conn = sqlite3.connect("./boveda.sqlite3",check_same_thread=False)

        self.cursor = self.conn.cursor()

    def comandos(self,texto):
        """Obtener comandos del comentario"""

        if "!" in texto:

            comandos = ["!tip","!saldo","!saldazo","!rank",
                        "!rankme","!rank25","!shop","!huachibono",
                        "!guild","!build","!asalto","!atraco",
                        "!levanton","!poker","!huachilate","!huachito",
                        "!huachilote","!rtd","!retiro",
                        "!deposito","!flair"]

            return [ comando for comando in comandos if comando in texto ]

        else:

            return None
    
    def error_log(self,error):
        """Actualizar el error log"""

        with open("./error_log.txt", "a", encoding="utf-8") as temp_file:
            temp_file.write(error + "\n")

    def buscar_log(self,comment_id):
        """Buscar si el comentario ha sido previamente procesado por el empleado del mes"""

        query = """SELECT * FROM comentarios WHERE id_comment=?"""

        resultado = self.cursor.execute(query,(comment_id,)).fetchall()

        if resultado != []:
            if comment_id == resultado[0][1]:
                return True
        
        elif resultado == []:
            return False        

    def actualizar_log(self,comment_id):
        """Agregar id de comentarios en el log"""

        query = """INSERT INTO comentarios (id_comment) VALUES (?)"""

        cursor = self.conn.cursor()

        cursor.execute(query,(comment_id,))

        self.conn.commit()
    
    def shop_item(self,remitente,destinatario,item):

        compra = shop(remitente,destinatario,item)

        return reddit.redditor(remitente).message("Ticket de Compra - Shop",compra)

    def shop_huachibono(self,remitente,clase,item):
                        
        bono = actualizar_huachibonos(remitente,clase,item)

        return reddit.redditor(remitente).message("Ticket de Compra - Huachibono",bono)

    def propina(self,texto,remitente,destinatario,id):
        
        try:
            #Extraemos la cantidad
            pattern = '!tip\ *(\d+)'

            result = re.findall(pattern, texto)

            cantidad = result[0]

            #Corroboramos que sea un numero
            if cantidad.isdigit():
                
                #Realizamos la transaccion
                transaccion = tip(remitente,destinatario,math.ceil(abs(float(cantidad))))
                   
                #Mensaje cuenta nueva
                if transaccion[0]:

                    reddit.redditor(destinatario).message("Bienvenid@ a la HuachiNet!", "Recueda que todo es pura diversion, amor al arte digital. Revisa el [post](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo responde: !historial a este mensaje")
                                    
                #Evitar que el empleado se responda a si mismo.
                if transaccion[1] == "autotip":
                    
                    pass
                
                else:

                    #Responder al cliente
                    reddit.redditor(remitente).message("Transaccion Exitosa",transaccion[1])
                        
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Tip - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
            
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def saldazo(self,remitente,id):
    
        try:
            consulta = saldazo(remitente)

            #Responder al cliente

            reddit.redditor(remitente).message("Saldazo",consulta)
                                
        except:

            #Enviar mensaje de error si el empleado no entendio lo que recibio
            
            mensaje = f"Saldazo - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
            
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))
    
    def rankme(self,remitente,id):

        try:

            rankme = rank(remitente,0)

            #Responder al cliente
            reddit.redditor(remitente).message("Su lugar en la HuachiNet:",rankme)


        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Rankme - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)

            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def rank25(self,remitente,id):                          
        
        try:
            rank25 = rank(remitente,25)

            #Responder al cliente
            reddit.redditor(remitente).message("Forbes Mujico Top 25",rank25)

        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Rank25 - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)

            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def rank(self,remitente,id):

        try:
            
            rank10 = rank(remitente,10)

            #Responder al cliente
            reddit.redditor(remitente).message("Forbes Mujico Top 10",rank10)

        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Rank - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)

            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def Shop(self,texto,remitente,destinatario,id):

        #Opciones del menu
        opciones = shops['opciones shop']

        if "menu" in texto:

            menu = shops['menu shop']

            #Enviar menu
            reddit.redditor(remitente).message(menu[0],menu[1])

            return None
                        
        for opcion in opciones:

            if opcion in texto:
                                    
                #Enviar regalo
                self.shop_item(remitente,destinatario,opcion)

    def huachibonos(self,texto,remitente,id):

        #huachibonos
        perks = shops['bonos perks']

        traits = shops['bonos traits']

        weapons = shops['bonos weapons']

        opciones = shops['bonos opciones']

        huachis = HuachiNet(remitente)

        try:
            
            if huachis.guild != "Normal":

                if "menu" in texto:

                    menu = shops[huachis.guild]

                    #Enviar menu
                    
                    reddit.redditor(remitente).message(menu[0],menu[1])
                    
                    return None
                                    
                for opcion in opciones:
                            
                    if opcion in texto:
                                    
                        if opcion in perks:
                            #comprar huachibono
                            self.shop_huachibono(remitente,"perk",perks[opcion])
                        
                        elif opcion in traits:
                            #comprar huachibono
                            self.shop_huachibono(remitente,"trait",traits[opcion])
                        
                        elif opcion in weapons:
                            #comprar huachibono
                            
                            self.shop_huachibono(remitente,"weapon",weapons[opcion])
            else:
                #No pertenece a un guild
                reddit.redditor(remitente).message("Oh no....","No perteneces a un clan, no hay huachibonos.\nUsa el comando !guild seguido de un clan: (otakos | nalgoticas | conductores | corvidos)")
                
                return None
                            
        except:
            
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Huachibono - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
            
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def guild(self,texto,remitente,id):

        try:
                                
            opciones = shops["bonos guilds"]

            for opcion in opciones.keys():

                if opcion in texto:

                    resultado = unirse_guild(remitente,opciones[opcion])
                                    
                    #Responder al cliente
                    reddit.redditor(remitente).message("Enhorabuena!",resultado)        

        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Guild - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)

            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def build(self,remitente,id):

        try:
                                
            resultado = check_build(remitente)
                                    
            #Responder al cliente
            reddit.redditor(remitente).message("Build Stats",resultado)

                                               
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Build - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)

            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))
                        
    def asaltos(self,cholo,victima,tipo,id):

        try:

            resultado = asalto(cholo,victima,tipo)

            if "Guild | Mujicano" in resultado:

                if "ganó" in resultado:

                    generar_im_dinero(cholo,victima,tipo)

                    url = upload_imgur()

                    respuesta_cirilo = resultado.split("\n\n")[0]

                    if url[0] == 200:

                        #Responder al cliente
                        reddit.comment(id).reply(f"[{respuesta_cirilo}]({url[1]})")

                    else:

                        reddit.comment(id).reply(resultado)

                if "Ganaste" in resultado or "putiza" in resultado:

                    generar_im_sin(cholo,victima,1)

                    url = upload_imgur()

                    respuesta_cirilo = resultado.split("\n\n")[0]

                    #Responder al cliente
                    if url[0] == 200:

                        #Responder al cliente
                        reddit.comment(id).reply(f"[{respuesta_cirilo}]({url[1]})")

                    else:

                        reddit.comment(id).reply(resultado)

                elif "Perdiste" in resultado:

                    generar_im_sin(cholo,victima,0)

                    url = upload_imgur()

                    respuesta_cirilo = resultado.split("\n\n")[0]

                    #Responder al cliente
                    if url[0] == 200:

                        #Responder al cliente
                        reddit.comment(id).reply(f"[{respuesta_cirilo}]({url[1]})")

                    else:

                        reddit.comment(id).reply(resultado)

            else:

                #Responder al cliente
                reddit.comment(id).reply(resultado)

        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio

            mensaje = f"Asalto - Usuario {cholo} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)

            reddit.redditor(cholo).message("Mensaje Error",random.choice(resp_empleado_error))

    def levanton(self,texto,cholo,id):

        #Realizar consulta
        try:
            victima = buscar_usuario(texto)

            resultado = asalto(cholo,victima,"levanton")

            #Responder al cliente
            reddit.comment(id).reply(resultado)
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio

            #error_log(f"Levanton - Usuario {str(comment.author)} - Comentario {str(comment.id)}" + traceback.format_exc())

            reddit.redditor(cholo).message("Mensaje Error",random.choice(resp_empleado_error))
                                   
    def huachito(self,texto,remitente,id):

        try:
            #Verificar cuantos se van a comprar
            try:
                #Extraemos la cantidad
                pattern = '!huachito\ *(\d+)'

                result = re.findall(pattern, texto)

                print(result)

                cantidad = abs(int(result[0]))
           
            except:
                
                cantidad = 1
                
            respuesta = "__Rasca y gana con Huachito - Loteria Mujicana__"
                
            if cantidad < 31:
                    
                for i in range(cantidad):
                                        
                    resultado = slots(remitente)
                        
                    respuesta +=  f"\n\n{resultado}\n\n***"
                        
                if cantidad < 6:
                            
                    #Responder al cliente en comentarios
                            
                    reddit.comment(id).reply(respuesta)
                                    
                else:
                            
                    #Responder al cliente por DM
                            
                    reddit.redditor(remitente).message(f"Compraste {cantidad} huachitos!",respuesta)
                                        
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Huachito - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
                                
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def poker(self,remitente,destinatario,id):

        try:

            resultado = pokermujicano(remitente,destinatario)

            #Responder al cliente
            reddit.comment(id).reply(resultado)


        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Poker - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
                                    
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def huachilate(self,texto,remitente,id):

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
                                    
                for i in range(cantidad):
                        
                    compra = huachilate(remitente)
                                    
                #Responder al cliente
                reddit.redditor(remitente).message(f"Compraste {cantidad} huachilate(s)!",compra)
                            
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            
            mensaje = f"Huachilate - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
                                
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def rollthedice(self,texto,remitente,id):

        try:
            #Extraemos la cantidad
            pattern = '!rtd\ *(\d+)'
                                
            result = re.findall(pattern, texto)

            numero = abs(int(result[0]))
                                
            if numero > 0 and numero < 7:
                                    
                #Realizamos la transaccion
                resultado = rollthedice(remitente,numero)
                                    
                #Responder al cliente
                reddit.comment(id).reply(resultado)          
                                            
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"RTD - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
            
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))
                        
    def flair(self,texto,remitente,id):

        try:
                                    
            resultado = cambiar_flair(remitente,texto)

            if remitente in resultado:
               
                #Enviar mensaje a UVE
                
                reddit.redditor("UnidadVictimasEsp").message("Solicitud User Flair",resultado)
                                
            else:

                reddit.redditor(remitente).message("Error",resultado)
                            
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Flair - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
            
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def deposito(self,texto,remitente,id):

        try:
            #Extraemos la cantidad
            pattern = '!deposito\ *(\d+)'
                                
            result = re.findall(pattern, texto)

            cantidad = abs(int(result[0]))
                                
            #Realizamos la transaccion
            resultado = deposito_bancadenas(remitente,cantidad)
                                    
            #Responder al cliente
            reddit.redditor(remitente).message("Bancadenas - Solicitud de deposito",resultado)         
                                            
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Deposito - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
            
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))

    def retiro(self,texto,remitente,id):

        try:
            #Extraemos la cantidad
            pattern = '!retiro\ *(\d+)'
                                
            result = re.findall(pattern, texto)

            cantidad = abs(int(result[0]))
                                
            #Realizamos la transaccion
            resultado = retiro_bancadenas(remitente,cantidad)
                                    
            #Responder al cliente
            reddit.redditor(remitente).message("Bancadenas - Solicitud de retiro",resultado)         
                                            
        except:
            #Enviar mensaje de error si el empleado no entendio lo que recibio
            mensaje = f"Retiro - Usuario {remitente} - Comentario {id}\n{traceback.format_exc()}"

            self.error_log(mensaje)
            
            reddit.redditor(remitente).message("Mensaje Error",random.choice(resp_empleado_error))