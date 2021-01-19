import math
import random
import re
import sqlite3
from datetime import datetime

import praw

import config
from core import HuachiNet

conn_log = sqlite3.connect("boveda.sqlite3")

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

monaschinas = open("./shop/monaschinas.txt", "r", encoding="utf-8").read().splitlines()

trapos = open("./shop/trapos.txt", "r", encoding="utf-8").read().splitlines()

furros = open("./shop/furro.txt", "r", encoding="utf-8").read().splitlines()

nalgoticas = open("./shop/nalgoticas.txt", "r", encoding="utf-8").read().splitlines()

curas = open("./shop/curas.txt", "r", encoding="utf-8").read().splitlines()

reddit = praw.Reddit(client_id=config.APP_ID, 
                     client_secret=config.APP_SECRET,
                     user_agent=config.USER_AGENT, 
                     username=config.REDDIT_USERNAME,
                     password=config.REDDIT_PASSWORD) 

def error_log(error):
    """Actualizar el error log"""

    with open("./error_log.txt", "a", encoding="utf-8") as temp_file:
        temp_file.write(error + "\n")

def buscar_log(comment_id):
    """Buscar si el comentario ha sido previamente procesado por el empleado del mes"""

    cursor = conn_log.cursor()

    query = """SELECT * FROM comentarios WHERE id_comment=?"""

    resultado = cursor.execute(query,(comment_id,)).fetchall()

    if resultado != []:
        if comment_id == resultado[0][1]:
            return True
        
    elif resultado == []:
        return False        

def actualizar_log(comment_id):
    """Agregar id de comentarios en el log"""

    cursor = conn_log.cursor()

    query = """INSERT INTO comentarios (id_comment) VALUES (?)"""

    cursor.execute(query,(comment_id,))

    conn_log.commit()

def saldazo(redditor_id) -> str:
    """Abierto todos los dias de 7am a 10pm"""
    
    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:
        return random.choice(resp_saldo) + f" {Huachis.saldo_total} Huachis"

def tip(remitente,destinatario,cantidad) -> str:
    """Dar propina por publicaciones y comentarios"""

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
                
                    reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")
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

    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:

        return (Huachis.historial,Huachis.saldo_total,Huachis.depositos,Huachis.retiros,Huachis.asaltos,Huachis.atracos,Huachis.huachitos,Huachis.premios_huachito,Huachis.levantones)

def rank(redditor_id, topten=False,top25=False) -> str:
    """Forbes Mujico - TOP Abinerados"""

    #Acceder a la HuachiNet
    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el redditor tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    #Ranking global
    if topten == True:

        #Respuesta en forma de string
        respuesta = "# Forbes Mujico - Top Ten Abinerados\n\nLugar | Mujican@ | Cantidad\n:--|:--:|--:\n"
        
        for i,item in enumerate(Huachis.Ranking(),start=1):

            respuesta += f"__{i}__ | {item[0]} | {item[1]:,} H¢N\n"

            if i == 10:
                break
                
        return respuesta
    
    if top25 == True:

        #Respuesta en forma de string
        respuesta = "# Forbes Mujico - Top 25 Abinerados\n\nLugar | Mujican@ | Cantidad\n:--|:--:|--:\n"
        
        for i,item in enumerate(Huachis.Ranking(),start=1):

            respuesta += f"__{i}__ | {item[0]} | {item[1]:,} H¢N\n"

            if i == 25:
                break
                
        return respuesta

    elif topten == False:
        #Ranking por usuario
        for i,item in enumerate(Huachis.Ranking(),start=1):

            if item[0] == redditor_id:

                return f"Tu posicion en la HuachiNet es la numero: __{i}__"

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

    for usuario in Huachis.Ranking():

        if resultado == usuario[0].lower():
            
            return usuario[0]

def empleado_del_mes():
    """El motor de nuestra huachieconomia"""       

    #Buscar subreddits
    for subreddit in config.SUBREDDITS:
       
        for comment in reddit.subreddit(subreddit).comments(limit=100):

            #Buscar si el comentario ha sido procesado previamante
            if buscar_log(str(comment.id)) == False:
                    
                #Buscar comandos
                if "!tip" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))
                        
                        try:
                            #Extraemos la cantidad
                            string = comment.body.lower()
                
                            pattern = '!tip\ *(\d+)'

                            result = re.findall(pattern, string)

                            cantidad = result[0]

                            #Corroboramos que sea un numero
                            if cantidad.isdigit():

                                #Realizamos la transaccion
                                transaccion = tip(str(comment.author),str(comment.parent().author),math.ceil(abs(float(cantidad))))

                                print(f'----\n{transaccion}')

                                #Evitar que el empleado se responda a si mismo.
                                if transaccion == "autotip":
                                    pass
                                
                                else:
                                    #Responder al cliente
                                    reddit.redditor(str(comment.author)).message("Transaccion Exitosa",transaccion)
                                    
                                        
                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))

                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                                
                            
                elif "!saldazo" in comment.body.lower() or "!saldo" in comment.body.lower():

                    if comment.author != None:
                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:
                            
                            consulta = saldazo(str(comment.author))

                            print(f'----\n{consulta}')

                            #Responder al cliente
                            reddit.redditor(str(comment.author)).message("Saldazo",consulta)
                            
                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))

                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                        
                                                   

                elif "!rankme" in comment.body.lower():

                    if comment.author != None:
                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            rankme = rank(str(comment.author))

                            print(f'----\n{rankme}')

                            #Responder al cliente
                            reddit.redditor(str(comment.author)).message("Tu lugar en la HuachiNet",rankme)

                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))

                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                            
                            
                elif "!rank25" in comment.body.lower():

                    if comment.author != None:
                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            rank25 = rank(str(comment.author),top25=True)

                            print(f'----\n{rank25}')

                            #Responder al cliente
                            reddit.redditor(str(comment.author)).message("Forbes Mujico Top 25",rank25)

                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))

                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                               


                elif "!rank" in comment.body.lower():

                    if comment.author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            rank10 = rank(str(comment.author),topten=True)

                            print(f'----\n{rank10}')

                            #Responder al cliente
                            reddit.redditor(str(comment.author)).message("Forbes Mujico Top 10",rank10)

                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))

                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                        
                                
                    
                elif "!shop monachina" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"monachina")

                        print(f'----\n{compra}')

                        reddit.redditor(str(comment.author)).message("Ticket de Compra",compra)
                                

                elif "!shop trapo" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"trapo")

                        print(f'----\n{compra}')

                        reddit.redditor(str(comment.author)).message("Ticket de Compra",compra)

                elif "!shop furro" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"furro")

                        print(f'----\n{compra}')

                        reddit.redditor(str(comment.author)).message("Ticket de Compra",compra)

                elif "!shop nalgotica" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"nalgotica")

                        print(f'----\n{compra}')

                        reddit.redditor(str(comment.author)).message("Ticket de Compra",compra)

                elif "!shop cura" in comment.body.lower() or "!shop corvido" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"cura")

                        print(f'----\n{compra}')

                        reddit.redditor(str(comment.author)).message("Ticket de Compra",compra)

                
                elif "!shop huachito" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"huachito")

                        print(f'----\n{compra}')

                        reddit.redditor(str(comment.author)).message("Ticket de Compra",compra)


                elif "!shop menu" in comment.body.lower():

                    if comment.parent().author != None:
                    
                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        reddit.redditor(str(comment.author)).message("Menu Shop","__HuachiStore - Abierto cuando llegamos, cerrado cuando nos vamos__\n\nEnvia un regalo usando el comando shop, seguido de una opcion del menu, todo a 5 huachis.\n\nRegalo | Comando\n:--|--:\nMonas Chinas | monachina\nTrapitos | trapo\nFurros | furro\nHuachito | huachito\nNalgoticas | nalgotica\nMDLP | cura / corvido\n\nCompleta tu compra de la siguiente manera:\n\n    shop comando\n\n    Ejemplo: shop monachina\n\n    (no olvides el signo de exclamación)\n\nUsalo en la seccion de comentarios.")
                    

                elif "!asalto" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            resultado = asalto(str(comment.author),str(comment.parent().author))

                            print(f'----\n{resultado}')

                            #Responder al cliente
                            comment.reply(resultado)

                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))

                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                            


                elif "!atraco" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            resultado = atraco(str(comment.author),str(comment.parent().author))

                            print(f'----\n{resultado}')

                            #Responder al cliente
                            comment.reply(resultado)

                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))

                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                elif "!levanton" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            victima = buscar_usuario(comment.body.lower())

                            resultado = levanton(str(comment.author),victima)

                            print(f'----\n{resultado}')

                            #Responder al cliente
                            comment.reply(resultado)

                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))

                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                            

                elif "!huachito" in comment.body.lower():

                    if comment.author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            resultado = slots(str(comment.author))

                            print(f'----\n{resultado}')

                            #Responder al cliente
                            comment.reply(resultado)

                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))
                            
                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                                              
                elif "!poker" in comment.body.lower():

                    if comment.author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            resultado = pokermujicano(str(comment.author))

                            print(f'----\n{resultado}')

                            #Responder al cliente
                            comment.reply(resultado)

                        except Exception as e:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            error_log(str(e))
                            
                            reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))
                                              
def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    for mensaje in reddit.inbox.unread(limit=100):

        #Buscar si el mensaje ha sido procesado previamante
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

                    chunk = f"__Saldo: {estado_cuenta[1]} Huachicoin(s)__\n\n**Total de movimientos**\n\nDepositos: {len(estado_cuenta[2])}    Retiros: {len(estado_cuenta[3])}\n\nAsaltos ganados: {len(asalto_victoria)}    Asaltos perdidos: {len(asalto_perdida)}\n\nAtracos ganados: {len(atraco_victoria)}    Atracos perdidos: {len(atraco_perdida)}\n\nHuachitos Comprados: {len(estado_cuenta[6])}    Huachitos Ganados: {len(estado_cuenta[7])}\n\nFecha | Nota | Cantidad | Destino / Origen\n:--|:--:|--:|:--:\n"

                    for i,item in enumerate(estado_cuenta[0],start=1):

                        chunk += f"{datetime.fromtimestamp(float(item[1])).ctime()} | {item[3]} | {item[2]} | {item[4]}\n"
                        
                        if len(estado_cuenta[0]) < 25:
                            
                            x = len(estado_cuenta[0])

                        else:

                            x = 25
                            
                        if i % x == 0:

                            reddit.redditor(str(mensaje.author)).message(f"Estado de Cuenta: {mensaje.author}",chunk)

                            break
                
            except Exception as e:
                #Mensaje no tienes cuenta
                error_log(e)

                mensaje.reply(random.choice(resp_tip_cuenta))

def shop(remitente,destinatario,regalo):
    """Tienda de regalos"""

    #Acceder a la HuachiNet
    Huachis = HuachiNet(remitente)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(remitente) == False:
        
        return random.choice(resp_tip_cuenta)

    else:
        #Verificar que se tenga saldo suficiente para la transaccion
        if Huachis.saldo_total < 5:

            return random.choice(resp_tip_sinbineros)

        else:

            #Iniciamos transaccion
            Huachis.Enviar_Bineros('Shop',5,nota=regalo.capitalize())
            
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

            elif regalo == 'huachito':

                huachito = slots(destinatario,regalo=True)

                reddit.redditor(destinatario).message("Te mandaron un regalito.....",f"{remitente} te ha enviado un huachito, que te diviertas rascando! \n\n {huachito}")

                return random.choice(resp_shop)

def asalto(cholo,victima):
    """Saca bineros morro"""

    if cholo == victima:
        #Respuesta en caso de autorobo
        return random.choice(resp_autorobo)

    #Proteger al CEO
    if victima == "MarcoCadenas" or victima == "Empleado_del_mes" or victima == 'Disentibot':
        
        return random.choice(resp_seguridad)

    else:

        morralla = random.randint(1,50)

        if cholo == "MarcoCadenas" or cholo == "AutoModerator" or cholo == "Empleado_del_mes":

            redditor_cholo = 101

        else:
            redditor_cholo = random.randint(1,100)

        redditor_victima = random.randint(1,100)

        if redditor_cholo > redditor_victima:
            #Acceder a la HuachiNet
            Huachis = HuachiNet(victima)

            #Primero verificar que el remitente tenga una cuenta
            if Huachis.Verificar_Usuario(victima) == False:
        
                return "No tiene cuenta, dime, que piensas robarle, ¿Los calzones?"

            else:
                #Verificar que se tenga saldo suficiente para la transaccion
                if Huachis.saldo_total < morralla:

                    return "Chale, asaltaste a alguien sin dinero, mal pedo."
            
                else:

                    if Huachis.Verificar_Usuario(cholo) == False:
                        #Abrimos cuenta y le damos dineros de bienvenida
                        Huachis.Bono_Bienvenida(cholo)
                
                        reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")
                    #Enviar Binero
                    Huachis.Enviar_Bineros(cholo,morralla,nota="Asalto")

                    return random.choice(resp_tumbar_cholo) + f"\n\n__{cholo} ganó {morralla} huachis (de la cartera de {victima})__" 

        else:
            #Acceder a la HuachiNet
            Huachis = HuachiNet(cholo)

            #Primero verificar que el remitente tenga una cuenta
            if Huachis.Verificar_Usuario(cholo) == False:
        
                return random.choice(resp_tip_cuenta)

            else:
                #Verificar que se tenga saldo suficiente para la transaccion
                if Huachis.saldo_total < morralla:

                    return "Perdiste, pero no tienes dinero que dar."
            
                else:

                    if Huachis.Verificar_Usuario(victima) == False:
                        #Abrimos cuenta y le damos dineros de bienvenida
                        Huachis.Bono_Bienvenida(victima)
                
                        reddit.redditor(victima).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el post sticky en Mujico para mas informacion de como usar la red.\n\nAqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: \n\n!historial o !saldo / !saldazo")
                
                    #Enviar Binero
                    Huachis.Enviar_Bineros(victima,morralla,nota="Asalto")

                    return random.choice(resp_tumbar_victima) + f"\n\n__{victima} ganó {morralla} huachis (de la cartera de {cholo})__"

def atraco(cholo,victima):
    """Asalto en esteroides"""

    if cholo == victima:
        #Respuesta en caso de autorobo
        return random.choice(resp_autorobo)

    #Proteger a los bots
    if victima == "MarcoCadenas" or victima == "Empleado_del_mes" or victima == "Disentibot" or victima == "AutoModerator":
        
        return random.choice(resp_seguridad)

    else:

        if cholo == "AutoModerator" or cholo == "MarcoCadenas" or cholo == "Empleado_del_mes":

            redditor_cholo = 101

        elif cholo == "Hastur082":

            redditor_cholo = 65
            
        else:

            redditor_cholo = random.randint(1,100)

        if victima == "Hastur082":

            redditor_victima = 65

        else:

            redditor_victima = random.randint(1,100)

        if redditor_cholo > redditor_victima:
            #Acceder a la HuachiNet
            Huachis = HuachiNet(victima)
            
            #Cantidad a perder
            cantidad = round(int(Huachis.saldo_total) * random.randint(5,16) / 100)

            if cantidad == 0:

                cantidad = 1

            #Primero verificar que la victima tenga una cuenta
            if Huachis.Verificar_Usuario(victima) == False:
        
                return "No tiene cuenta, dime, que piensas robarle, ¿Los calzones?"

            else:
                #Verificar que el saldo sea suficiente
                if Huachis.saldo_total == 0:

                    return "Chale, asaltaste a alguien sin dinero, mal pedo."
            
                else:

                    if Huachis.Verificar_Usuario(cholo) == False:
                        #Abrimos cuenta y le damos dineros de bienvenida
                        Huachis.Bono_Bienvenida(cholo)
                
                        reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")
                    #Enviar Binero
                    Huachis.Enviar_Bineros(cholo,cantidad,nota="Atraco")

                    return random.choice(resp_tumbar_cholo) + f"\n\n__{cholo} ganó {cantidad} huachis (de la cartera de {victima})__" 

        else:
            #Acceder a la HuachiNet
            Huachis = HuachiNet(cholo)

            #Cantidad a perder
            cantidad = round(int(Huachis.saldo_total) * random.randint(5,16) / 100)

            if cantidad == 0:

                cantidad = 1

            #Primero verificar que el cholo tenga una cuenta
            if Huachis.Verificar_Usuario(cholo) == False:
        
                return random.choice(resp_tip_cuenta)

            else:
                #Verificar que se tenga saldo suficiente para la transaccion
                if Huachis.saldo_total == 0:

                    return "Perdiste, pero no tienes dinero que dar."
            
                else:

                    if Huachis.Verificar_Usuario(victima) == False:
                        #Abrimos cuenta y le damos dineros de bienvenida
                        Huachis.Bono_Bienvenida(victima)
                
                        reddit.redditor(victima).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el post sticky en Mujico para mas informacion de como usar la red.\n\nAqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: \n\n!historial o !saldo / !saldazo")
                
                    #Enviar Binero
                    Huachis.Enviar_Bineros(victima,cantidad,nota="Atraco")

                    return random.choice(resp_tumbar_victima) + f"\n\n__{victima} ganó {cantidad} huachis (de la cartera de {cholo})__"

def slots(redditor_id,regalo=False):
    """Ahora si es todo un casino"""

    if regalo != True:

        #Acceder a cuenta del redditor
        Huachis_redditor = HuachiNet(redditor_id)
        
        #Verificar que tenga cuenta
        if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
            return random.choice(resp_tip_cuenta)

        else: 
            #Verificar que tenga saldo
            if Huachis_redditor.saldo_total < 5:
            
                return random.choice(resp_tip_sinbineros)

            else:
                #Cobrar el Huachito
                Huachis_redditor.Enviar_Bineros("Shop",5,nota="Huachito")

    emojis = ['👻','🐷','🐧','🦝','🍮', '💣','👾','👽','🦖','🥓','🤖']

    huachito = [random.choice(emojis) for i in range(5)]

    conteo = [huachito.count(emoji) for emoji in emojis if huachito.count(emoji) != 0 and emoji != '🥓']
    
    #Contar cuantos tocinos hay en el huachito
    if '🥓' in huachito:
        maximo = max(conteo)

        tocinos = huachito.count('🥓')

        conteo.append(maximo + tocinos)


    if huachito.count('💣') > 1:
        #Enviar mensaje de perdida en caso de 2 o mas bombas
        respuestas_bomba = ["Como en buscaminas, te explotaron las bombas, perdiste!","Varias bombas werito, perdiste","BOMBA! mala suerte :'(","Te salio el negrito y el prietito del arroz, perdistes."]

        return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!{random.choice(respuestas_bomba)}!<"
                
    else:
        #Entregar premios
        maximo = max(conteo)
                    
        if maximo == 3:
            #Acceder a cuenta shop
            Huachis_shop = HuachiNet("Shop")

            if huachito.count('👻') == 3:
                cantidad = 300
                            
            elif huachito.count('🐷') == 3:
                cantidad = 70

            elif huachito.count('🍮') == 3:
                cantidad = 80

            elif huachito.count('🦝') == 3:
                cantidad = 150

            elif huachito.count('👾') == 3:
                cantidad = 90

            elif huachito.count('👽') == 3:
                cantidad = 100

            elif huachito.count('🦖') == 3:
                cantidad = 200

            elif huachito.count('🐧') == 3:
                cantidad = 60

            elif huachito.count('🤖') == 3:
                cantidad = 50

            else:
                cantidad = 30
                            
            if '💣' in huachito:
                cantidad = round(cantidad / 2)

            if Huachis_shop.Verificar_Usuario(redditor_id) == False:
                #Abrimos cuenta y le damos dineros de bienvenida
                Huachis_shop.Bono_Bienvenida(redditor_id)
                
                reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")            
            Huachis_shop.Enviar_Bineros(redditor_id,cantidad,nota="Premio Huachito")

            if '🥓' in huachito:

                return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste {cantidad:,} huachis (3 iguales usando comodin 🥓)!<"
                    
            else:

                return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste {cantidad:,} huachis (3 iguales)!<"

        elif maximo == 4:

            #Acceder a cuenta shop
            Huachis_shop = HuachiNet("Shop")

            if huachito.count('👻') == 4:
                cantidad = 4000
                            
            elif huachito.count('🐷') == 4:
                cantidad = 800

            elif huachito.count('🍮') == 4:
                cantidad = 900

            elif huachito.count('🦝') == 4:
                cantidad = 2000

            elif huachito.count('👾') == 4:
                cantidad = 1000

            elif huachito.count('👽') == 4:
                cantidad = 1500

            elif huachito.count('🦖') == 4:
                cantidad = 3000

            elif huachito.count('🐧') == 4:
                cantidad = 700

            elif huachito.count('🤖') == 4:
                cantidad = 600

            else:
                cantidad = 500
                            
            if '💣' in huachito:
                cantidad = round(cantidad / 2)

            if Huachis_shop.Verificar_Usuario(redditor_id) == False:
                #Abrimos cuenta y le damos dineros de bienvenida
                Huachis_shop.Bono_Bienvenida(redditor_id)
                
                reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")
            Huachis_shop.Enviar_Bineros(redditor_id,cantidad,nota="Premio Huachito")
            
            if '🥓' in huachito:

                return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste {cantidad:,} huachis (4 iguales usando comodin 🥓)!<"
                    
            else:

                return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste {cantidad:,} huachis (4 iguales)!<"

        elif maximo == 5:

            #Acceder a cuenta shop
            Huachis_shop = HuachiNet("Shop")

            if huachito.count('👻') == 5:
                cantidad = 10000
                            
            elif huachito.count('🐷') == 5:
                cantidad = 4000

            elif huachito.count('🍮') == 5:
                cantidad = 5000

            elif huachito.count('🦝') == 5:
                cantidad = 8000

            elif huachito.count('👾') == 5:
                cantidad = 6000

            elif huachito.count('👽') == 5:
                cantidad = 7000

            elif huachito.count('🦖') == 5:
                cantidad = 9000

            elif huachito.count('🐧') == 5:
                cantidad = 3000

            elif huachito.count('🤖') == 5:
                cantidad = 2000

            else:
                cantidad = 1000
                            
            if '💣' in huachito:
                cantidad = round(cantidad / 2)

            if Huachis_shop.Verificar_Usuario(redditor_id) == False:
                #Abrimos cuenta y le damos dineros de bienvenida
                Huachis_shop.Bono_Bienvenida(redditor_id)
                
                reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")
            Huachis_shop.Enviar_Bineros(redditor_id,cantidad,nota="Premio Huachito")

            if '🥓' in huachito:

                return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste {cantidad:,} huachis (5 iguales usando comodin 🥓)!<"
                    
            else:

                return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste {cantidad:,} huachis (5 iguales)!<"

        #Dar dinero en caso de 2 pares iguales
        elif conteo.count(2) == 2:
            #Acceder a cuenta shop
            Huachis_shop = HuachiNet("Shop")

            if '💣' in huachito:
                cantidad = 5
            else:
                cantidad = 10

            if Huachis_shop.Verificar_Usuario(redditor_id) == False:
                #Abrimos cuenta y le damos dineros de bienvenida
                Huachis_shop.Bono_Bienvenida(redditor_id)
                
                reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")

            Huachis_shop.Enviar_Bineros(redditor_id,cantidad,nota="Premio Huachito")
            

            if '🥓' in huachito:

                return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste {cantidad:,} huachis (2 pares iguales usando comodin 🥓)!<"
                    
            else:

                return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste {cantidad:,} huachis (2 pares iguales)!<"

        respuestas_perdida = ["Sigue participando","Suerte para la proxima","Asi es el negocio de rascar boletitos, llevate un dulce del mostrador"]

        return f"__Rasca y gana con Huachito - Loteria Mujicana__\n\n>!{' '.join(huachito)}!<\n\n>!{random.choice(respuestas_perdida)}!<"

def levanton(cholo,victima):
    """Dar un levanton a los usuarios alterados"""

    if victima == 'None':
        return "Patron, me parece que esa persona no existe."

    if cholo == victima:
        #Respuesta en caso de autorobo
        return random.choice(resp_autorobo)

    #Proteger a los bots
    if victima == "MarcoCadenas" or victima == "Empleado_del_mes" or victima == "Disentibot" or victima == "AutoModerator":
        
        return random.choice(resp_seguridad)

    else:

        if cholo == "AutoModerator" or cholo == "MarcoCadenas" or cholo == "Empleado_del_mes":

            redditor_cholo = 101
            
        else:

            redditor_cholo = random.randint(1,100)


        redditor_victima = random.randint(1,100)

        if redditor_cholo > redditor_victima:
            #Acceder a la HuachiNet
            Huachis = HuachiNet(victima)
            
            #Cantidad a perder
            cantidad = round(int(Huachis.saldo_total) * 16 / 100)

            if cantidad == 0:

                cantidad = 1

            #Primero verificar que la victima tenga una cuenta
            if Huachis.Verificar_Usuario(victima) == False:
        
                return "No tiene cuenta, dime, que piensas robarle, ¿Los calzones?"

            else:
                #Verificar que el saldo sea suficiente
                if Huachis.saldo_total == 0:

                    return "Chale, asaltaste a alguien sin dinero, mal pedo."
            
                else:

                    if Huachis.Verificar_Usuario(cholo) == False:
                        #Abrimos cuenta y le damos dineros de bienvenida
                        Huachis.Bono_Bienvenida(cholo)
                
                        reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")
                    #Enviar Binero
                    Huachis.Enviar_Bineros(cholo,cantidad,nota="Levanton")

                    return random.choice(resp_levanton) + f"\n\n__{cholo} ganó {cantidad} huachis (de la cartera de {victima})__" 

        else:
            #Acceder a la HuachiNet
            Huachis = HuachiNet(cholo)

            #Cantidad a perder
            cantidad = round(int(Huachis.saldo_total) * 16 / 100)

            if cantidad == 0:

                cantidad = 1

            #Primero verificar que el cholo tenga una cuenta
            if Huachis.Verificar_Usuario(cholo) == False:
        
                return random.choice(resp_tip_cuenta)

            else:
                #Verificar que se tenga saldo suficiente para la transaccion
                if Huachis.saldo_total == 0:

                    return "Perdiste, pero no tienes dinero que dar."
            
                else:

                    if Huachis.Verificar_Usuario(victima) == False:
                        #Abrimos cuenta y le damos dineros de bienvenida
                        Huachis.Bono_Bienvenida(victima)
                
                        reddit.redditor(redditor_id).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial")
                    #Enviar Binero
                    Huachis.Enviar_Bineros(victima,cantidad,nota="Levanton")

                    return random.choice(resp_tumbar_victima) + f"\n\n__{victima} ganó {cantidad} huachis (de la cartera de {cholo})__"

def pokermujicano(redditor_id):

    #Acceder a cuenta del redditor
    Huachis_redditor = HuachiNet(redditor_id)
        
    #Verificar que tenga cuenta
    if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else: 
        #Verificar que tenga saldo
        if Huachis_redditor.saldo_total < 5:
            
            return random.choice(resp_tip_sinbineros)

        else:
            #Cobrar la entrada
            cantidad = random.randint(20,200)
            Huachis_redditor.Enviar_Bineros("Shop",cantidad,nota="Poker")
            
    
    valores = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    baraja = [[('♠',valor,"espada") for valor in valores],
              [('♥',valor,"corazon") for valor in valores],
              [('♦',valor,"diamante") for valor in valores],
              [('♣',valor,"trebol") for valor in valores]]

    cartas = [carta for palo in baraja for carta in palo]

    for i in range(100):
        random.shuffle(cartas)

    manos = random.sample(cartas,k=10)

    casa = combinaciones_poker(manos[0:5])

    redditor = combinaciones_poker(manos[5:10])

    cartas_casa = f'{manos[0][0]} : {manos[0][1]} | {manos[1][0]} : {manos[1][1]} | {manos[2][0]} : {manos[2][1]} | {manos[3][0]} : {manos[3][1]} | {manos[4][0]} : {manos[4][1]}'

    cartas_redditor = f'{manos[5][0]} : {manos[5][1]} | {manos[6][0]} : {manos[6][1]} | {manos[7][0]} : {manos[7][1]} | {manos[8][0]} : {manos[8][1]} | {manos[9][0]} : {manos[9][1]}'

    if casa[0][1] > redditor[0][1]:

        return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para el empleado, usando {casa[0][0]}\n\n_Pot: {cantidad} huachicoins_' 

    elif casa[0][1] < redditor[0][1]:

        #Acceder a la cuenta de la shop
        Huachis_shop = HuachiNet("Shop")

        Huachis_shop.Enviar_Bineros(redditor_id,cantidad,nota="Poker")
        
        return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para {redditor_id}, usando {redditor[0][0]}\n\n_Pot: {cantidad} huachicoins_'

    elif casa[0][1] == redditor[0][1]:

        if max(casa[1]) > max(redditor[1]):

            return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para el empleado, usando {casa[0][0]}\n\n_Pot: {cantidad} huachicoins_' 

        elif max(casa[1] < max(redditor[1])):

            #Acceder a la cuenta de la shop
            Huachis_shop = HuachiNet("Shop")

            Huachis_shop.Enviar_Bineros(redditor_id,cantidad,nota="Poker")

            return f'_Poker Estilo Mujico_\n\nMano del empleado:\n\n{cartas_casa}\n\nMano de {redditor_id}\n\n{cartas_redditor}\n\nVictoria para {redditor_id}, usando {redditor[0][0]}\n\n_Pot: {cantidad} huachicoins_'

        elif max(casa[1] == max(redditor[1])):

            return "Empate tecnico, mi patron no me programo algo para esta situacion, no hay devoluciones es politica de la empresa, lo siento. A si que perdiste"

        
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

                return (puntaje,valores_corregidos)
        
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

                    return (puntaje,valores_corregidos)
                
                else:
                    #Puntaje Color
                    puntaje = ("Color",6)

                    return (puntaje,valores_corregidos)

    #Full House 
    fullhouse = 0
    for valor in valores:

        if valores_cartas.count(valor) == 3:
            fullhouse += 3
        
        elif valores_cartas.count(valor) == 2:
            fullhouse += 2

    if fullhouse == 5:
        #Puntaje Fullhouse
        puntaje = ("Full House",7)

        return (puntaje,valores_corregidos)

    #Escalera
    #Contar numeros consecutivos
    escalera = 0
    #Escalera alta con A
    if "A" in valores_cartas and "K" in valores_cartas and "Q" in valores_cartas and "J" in valores_cartas and "10" in valores_cartas:
        #Puntaje escalera alta
        puntaje = ("Escalera Alta",5)

        return (puntaje,valores_corregidos)

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

            return (puntaje,valores_corregidos)

    #Poker / Tercia / Dos pares / Pares
    pares = 0

    for valor in valores:
        if valores_cartas.count(valor) ==  4:
            #Poker
            puntaje = ("Poker",8)

            return (puntaje,valores_corregidos)

        if valores_cartas.count(valor) ==  3:
            #Tercia
            puntaje = ("Tercia",4)

            return (puntaje,valores_corregidos)

        if valores_cartas.count(valor) ==  2:
            #Sumar par
            pares += 1

    if pares == 2:
        #Puntaje dos pares
        puntaje = ("Dos Pares",3)

        return (puntaje,valores_corregidos)
    
    elif pares == 1:
        #Puntaje pares
        puntaje = ("Pares",2)

        return (puntaje,valores_corregidos)
    
    puntaje = ("Carta Alta",1)

    return (puntaje,valores_corregidos)

if __name__ == "__main__":
    
    empleado_del_mes()

    print("\nTransacciones al corriente señor!")

    servicio_al_cliente()

    print("\nYa respondi a todas las quejas patron!")





