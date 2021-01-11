from core import HuachiNet
import praw
import config
import sqlite3
import re
from datetime import datetime
import random

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

monaschinas = open("./shop/monaschinas.txt", "r", encoding="utf-8").read().splitlines()

trapos = open("./shop/trapos.txt", "r", encoding="utf-8").read().splitlines()

furros = open("./shop/furro.txt", "r", encoding="utf-8").read().splitlines()

reddit = praw.Reddit(client_id=config.APP_ID, 
                     client_secret=config.APP_SECRET,
                     user_agent=config.USER_AGENT, 
                     username=config.REDDIT_USERNAME,
                     password=config.REDDIT_PASSWORD) 

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
        return random.choice(resp_saldo) + f" {Huachis.saldo_total} Huachicoin(s)"

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
                
                    reddit.redditor(destinatario).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el post sticky en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial o !saldo / !saldazo")
            
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

        return (Huachis.historial,Huachis.saldo_total,Huachis.depositos,Huachis.retiros,Huachis.asaltos)

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

def empleado_del_mes():
    """El motor de nuestra huachieconomia"""       

    #Buscar subreddits
    for subreddit in config.SUBREDDITS:
       
        for comment in reddit.subreddit(subreddit).comments(limit=200):

            #Buscar si el comentario ha sido procesado previamante
            if buscar_log(str(comment.id)) == False:
                    
                #Buscar comandos
                if "!tip" in comment.body.lower():

                    if comment.parent().author != None:
                        try:
                            #Extraemos la cantidad
                            string = comment.body.lower()
                
                            pattern = '!tip\ *(\d+)'

                            result = re.findall(pattern, string)

                            cantidad = result[0]

                            #Corroboramos que sea un numero
                            if cantidad.isdigit():

                                #Agregar comentario al log
                                actualizar_log(str(comment.id))

                                #Realizamos la transaccion
                                transaccion = tip(str(comment.author),str(comment.parent().author),abs(int(cantidad)))

                                print(f'----\n{transaccion}')

                                #Evitar que el empleado se responda a si mismo.
                                if transaccion == "autotip":
                                    pass
                                
                                else:
                                    #Responder al cliente
                                    comment.reply(transaccion)
                                    
                                    
                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                                
                            
                elif "!saldazo" in comment.body.lower() or "!saldo" in comment.body.lower():

                    if comment.author != None:
                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:
                            
                            consulta = saldazo(str(comment.author))

                            print(f'----\n{consulta}')

                            #Responder al cliente
                            comment.reply(consulta)
                            
                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                        
                                                   

                elif "!rankme" in comment.body.lower():

                    if comment.author != None:
                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            rankme = rank(str(comment.author))

                            print(f'----\n{rankme}')

                            #Responder al cliente
                            comment.reply(rankme)

                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                            
                            
                elif "!rank25" in comment.body.lower():

                    if comment.author != None:
                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            rank25 = rank(str(comment.author),top25=True)

                            print(f'----\n{rank25}')

                            #Responder al cliente
                            comment.reply(rank25)

                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                               


                elif "!rank" in comment.body.lower():

                    if comment.author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            rank10 = rank(str(comment.author),topten=True)

                            print(f'----\n{rank10}')

                            #Responder al cliente
                            comment.reply(rank10)

                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                        
                                
                    
                elif "!shop monachina" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"monachina")

                        print(f'----\n{compra}')

                        comment.reply(compra)
                                

                elif "!shop trapo" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"trapo")

                        print(f'----\n{compra}')

                        comment.reply(compra)

                elif "!shop furro" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        compra = shop(str(comment.author),str(comment.parent().author),"furro")

                        print(f'----\n{compra}')

                        comment.reply(compra)


                elif "!shop menu" in comment.body.lower():

                    if comment.parent().author != None:
                    
                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        comment.reply("# HuachiStore - Abierto cuando llegamos, cerrado cuando nos vamos\n\nEnvia un regalo usando el comando shop, seguido de una opcion del menu, todo a 5 huachis.\n\nRegalo | Comando\n:--|--:\nMonas Chinas | monachina\nTrapitos | trapo\nFurros | furro\n\nCompleta tu compra de la siguiente manera:\n\n    shop comando\n\n    Ejemplo: shop monachina\n\n    (no olvides el signo de exclamación)\n\nNo respondas a este comentario.")
                    

                elif "!asalto" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            asalto = tumbar(str(comment.author),str(comment.parent().author))

                            print(f'----\n{asalto}')

                            #Responder al cliente
                            comment.reply(asalto)

                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                            


                elif "!atraco" in comment.body.lower():

                    if comment.parent().author != None:

                        #Agregar comentario al log
                        actualizar_log(str(comment.id))

                        #Realizar consulta
                        try:

                            asalto = atraco(str(comment.author),str(comment.parent().author))

                            print(f'----\n{asalto}')

                            #Responder al cliente
                            comment.reply(asalto)

                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                            

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

                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                                              
def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    for mensaje in reddit.inbox.messages(limit=10):

        #Buscar si el mensaje ha sido procesado previamante
        if buscar_log(str(mensaje.id)) == False:

            #Agregar mensaje al log
            actualizar_log(str(mensaje.id))

            try:

                if "!historial" in mensaje.body:

                    estado_cuenta = historial(str(mensaje.author))

                    asalto_victoria = [item for item in estado_cuenta[4] if item[2] == 5]

                    asalto_perdida = [item for item in estado_cuenta[4] if item[2] == -5]

                    mensaje.reply(f"Estado de Cuenta: {mensaje.author}\n\nSaldo: {estado_cuenta[1]} Huachicoin(s)\n\nCantidad de Depositos: {len(estado_cuenta[2])}\n\nCantidad de Retiros: {len(estado_cuenta[3])}\n\nCantidad de asaltos ganados: {len(asalto_victoria)}\n\nCantidad de asaltos perdidos: {len(asalto_perdida)}")

                    chunk = "Fecha | Nota | Cantidad | Destino / Origen\n:--|:--:|--:|:--:\n"

                    for i,item in enumerate(estado_cuenta[0],start=1):

                        chunk += f"{datetime.fromtimestamp(float(item[1])).ctime()} | {item[3]} | {item[2]} | {item[4]}\n"
                        
                        if len(estado_cuenta[0]) < 15:
                            
                            x = len(estado_cuenta[0])

                        else:

                            x = 15
                            
                        if i % x == 0:

                            mensaje.reply(chunk)

                            chunk = "Fecha | Nota | Cantidad | Destino / Origen\n:--|:--:|--:|:--:\n"
                
            except:
                #Mensaje no tienes cuenta
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
            Huachis.Enviar_Bineros('Shop',5)

            if regalo == 'monachina':

                monachina = random.choice(monaschinas)

                reddit.redditor(destinatario).message("Te han enviado un regalito.....",f"{remitente} te ha enviado una mona china! Kawaii desu ne! \n\n [Abrir Regalo]({monachina})")

                return random.choice(resp_shop)

            elif regalo == 'trapo':

                trapo = random.choice(trapos)

                reddit.redditor(destinatario).message("Te han enviado un regalito.....",f"{remitente} te ha enviado una dama con rama, no tengas miedo papi, si la agarras no da toques. \n\n [Abrir Regalo]({trapo})")

                return random.choice(resp_shop)

            elif regalo == 'furro':

                furro = random.choice(furros)

                reddit.redditor(destinatario).message("Te han enviado un regalito.....",f"{remitente} te ha enviado un furro, que te diviertas! \n\n [Abrir Regalo]({furro})")

                return random.choice(resp_shop)

def tumbar(cholo,victima):
    """Saca 5 varos morro"""

    if cholo == victima:
        #Respuesta en caso de autorobo
        return random.choice(resp_autorobo)

    #Proteger al CEO
    if victima == "MarcoCadenas" or victima == "Empleado_del_mes" or victima == 'Disentibot':
        
        return random.choice(resp_seguridad)

    else:

        morralla = random.randint(1,50)

        if cholo == "MarcoCadenas":

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
                
                        reddit.redditor(cholo).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el post sticky en Mujico para mas informacion de como usar la red.\n\nAqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: \n\n!historial o !saldo / !saldazo")
                
                    #Enviar Binero
                    Huachis.Enviar_Bineros(cholo,morralla,asalto=True)

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
                    Huachis.Enviar_Bineros(victima,morralla,asalto=True)

                    return random.choice(resp_tumbar_victima) + f"\n\n__{victima} ganó {morralla} huachis (de la cartera de {cholo})__"

def atraco(cholo,victima):
    """Asalto en esteroides"""

    if cholo == victima:
        #Respuesta en caso de autorobo
        return random.choice(resp_autorobo)

    #Proteger al CEO
    if victima == "MarcoCadenas" or victima == "Empleado_del_mes" or victima == "Disentibot":
        
        return random.choice(resp_seguridad)

    else:

        if cholo == "MarcoCadenas":

            redditor_cholo = 101

        else:

            redditor_cholo = random.randint(1,100)

        redditor_victima = random.randint(1,100)

        if redditor_cholo > redditor_victima:
            #Acceder a la HuachiNet
            Huachis = HuachiNet(victima)
            
            #Cantidad a perder
            cantidad = round(int(Huachis.saldo_total) * random.randint(5,16) / 100)

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
                
                        reddit.redditor(cholo).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el post sticky en Mujico para mas informacion de como usar la red.\n\nAqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: \n\n!historial o !saldo / !saldazo")
                
                    #Enviar Binero
                    Huachis.Enviar_Bineros(cholo,cantidad,asalto=True)

                    return random.choice(resp_tumbar_cholo) + f"\n\n__{cholo} ganó {cantidad} huachis (de la cartera de {victima})__" 

        else:
            #Acceder a la HuachiNet
            Huachis = HuachiNet(cholo)

            #Cantidad a perder
            cantidad = round(int(Huachis.saldo_total) * random.randint(5,16) / 100)

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
                    Huachis.Enviar_Bineros(victima,cantidad,asalto=True)

                    return random.choice(resp_tumbar_victima) + f"\n\n__{victima} ganó {cantidad} huachis (de la cartera de {cholo})__"

def slots(redditor_id):
    """Ahora si es todo un casino"""

    #Acceder a cuenta del redditor
    Huachis_redditor = HuachiNet(redditor_id)
    #Verificar que tenga cuenta
    if Huachis_redditor.Verificar_Usuario(redditor_id) == False:
        
        return random.choice(resp_tip_cuenta)

    else:
        #Verificar que tenga saldo
        if Huachis_redditor.saldo_total < 10:
            
            return random.choice(resp_tip_sinbineros)

        else:
            #Cobrar el Huachito
            Huachis_redditor.Enviar_Bineros("Shop",5)
        
            emojis = ['👻','👽','🐷','🦖','🐧','🦝','🍮', '💣','👾']

            huachito = [random.choice(emojis) for i in range(6)]

            conteo = [huachito.count(emoji) for emoji in emojis if huachito.count(emoji) != 0]

            if '💣' in huachito:
                #Enviar mensaje en caso de bomba
                respuestas_bomba = ["Como en buscaminas, te exploto la bomba, perdiste!","Te toco la bomba werito","BOMBA! mala suerte :'(","Te salio el negrito del arroz, perdistes."]

                return f"Aqui tienes tu huachito\n\n>!{' '.join(huachito)}!<\n\n>!{random.choice(respuestas_bomba)}!<"
                
            else:
                #Dar dinero en caso de 2 pares iguales
                if conteo.count(2) == 2:
                    #Acceder a cuenta shop
                    Huachis_shop = HuachiNet("Shop")

                    Huachis_shop.Enviar_Bineros(redditor_id,10,huachito=True)

                    return f"Aqui tienes tu huachito\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste 10 huachis (2 pares iguales)!<"

                elif conteo.count(2) == 3:
                    #Acceder a cuenta shop
                    Huachis_shop = HuachiNet("Shop")

                    Huachis_shop.Enviar_Bineros(redditor_id,100,huachito=True)

                    return f"Aqui tienes tu huachito\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste 10 huachis (3 pares iguales)!<"
                
                else:

                    for numero in conteo:
                        #Entregar premios

                        if numero == 3:
                            #Acceder a cuenta shop
                            Huachis_shop = HuachiNet("Shop")

                            Huachis_shop.Enviar_Bineros(redditor_id,50,huachito=True)

                            return f"Aqui tienes tu huachito\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste 50 huachis (3 iguales)!<"

                        elif numero == 4:

                            #Acceder a cuenta shop
                            Huachis_shop = HuachiNet("Shop")

                            Huachis_shop.Enviar_Bineros(redditor_id,300,huachito=True)

                            return f"Aqui tienes tu huachito\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste 300 huachis (4 iguales)!<"

                        elif numero == 5:

                            #Acceder a cuenta shop
                            Huachis_shop = HuachiNet("Shop")

                            Huachis_shop.Enviar_Bineros(redditor_id,1000,huachito=True)

                            return f"Aqui tienes tu huachito\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste 1000 huachis (5 iguales)!<"

                        elif numero == 6:

                            #Acceder a cuenta shop
                            Huachis_shop = HuachiNet("Shop")

                            Huachis_shop.Enviar_Bineros(redditor_id,10000,huachito=True)

                            return f"Aqui tienes tu huachito\n\n>!{' '.join(huachito)}!<\n\n>!Ganaste 10,000 huachis (Premio Mayor)!<"
                    
                    
                    respuestas_perdida = ["Sigue participando","Suerte para la proxima","Asi es este negocio de rascar boletitos, llevate un dulce del mostrador"]

                    return f"Aqui tienes tu huachito\n\n>!{' '.join(huachito)}!<\n\n>!{random.choice(respuestas_perdida)}!<"



if __name__ == "__main__":
    
    empleado_del_mes()

    print("\nTransacciones al corriente señor!")

    servicio_al_cliente()

    print("\nYa respondi a todas las quejas patron!")





