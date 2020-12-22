from core import HuachiNet
import praw
import config
import sqlite3
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

monaschinas = open("./shop/monaschinas.txt", "r", encoding="utf-8").read().splitlines()

reddit = praw.Reddit(client_id=config.APP_ID, client_secret=config.APP_SECRET,
                             user_agent=config.USER_AGENT, username=config.REDDIT_USERNAME,
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

        return (Huachis.historial,Huachis.saldo_total,Huachis.depositos,Huachis.retiros)

def rank(redditor_id, topten=False) -> str:
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

    elif topten == False:
        #Ranking por usuario
        for i,item in enumerate(Huachis.Ranking(),start=1):

            if item[0] == redditor_id:

                return f"Tu posicion en la HuachiNet es la numero: __{i}__"

def empleado_del_mes():
    """El motor de nuestra huachieconomia"""       

    #Buscar subreddits
    for subreddit in config.SUBREDDITS:
       
        for comment in reddit.subreddit(subreddit).comments(limit=100):
            
            #Buscar si el comentario ha sido procesado previamante
            if buscar_log(str(comment.id)) == False:
                
                #Agregar comentario al log
                actualizar_log(str(comment.id))

                #Buscar comandos
                if "!tip" in comment.body:
                    
                    #Realizar transaccion
                    try:
                        string = str(comment.body)
            
                        start = string.index("!tip")

                        cantidad = int(string[start:].replace("!tip","").strip())

                        transaccion = tip(str(comment.author),str(comment.parent().author),abs(cantidad))

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
                        
                        

                elif "!saldo" in comment.body or "!saldazo" in comment.body:

                    #Realizar consulta
                    try:
                        
                        consulta = saldazo(str(comment.author))

                        print(f'----\n{consulta}')

                        #Responder al cliente
                        comment.reply(consulta)
                        
                    except:
                        #Enviar mensaje de error si el empleado no entendio lo que recibio
                        comment.reply(random.choice(resp_empleado_error))
                        
                        

                elif "!rankme" in comment.body:

                    #Realizar consulta
                    try:

                        rankme = rank(str(comment.author))

                        print(f'----\n{rankme}')

                        #Responder al cliente
                        comment.reply(rankme)

                    except:
                        #Enviar mensaje de error si el empleado no entendio lo que recibio
                        comment.reply(random.choice(resp_empleado_error))
                        
                        

                elif "!rank" in comment.body:

                    #Realizar consulta
                    try:

                        rankg = rank(str(comment.author),topten=True)

                        print(f'----\n{rankg}')

                        #Responder al cliente
                        comment.reply(rankg)

                    except:
                        #Enviar mensaje de error si el empleado no entendio lo que recibio
                        comment.reply(random.choice(resp_empleado_error))
                        
                        

                elif "!shop" in comment.body:
                    
                    #Realizar transaccion
                    try:
                        string = str(comment.body.lower())
            
                        start = string.index("!shop")

                        opcion = string[start:].replace("!shop","").strip()

                        if opcion == "":

                            comment.reply("# HuachiStore - Abierto cuando llegamos, cerrado cuando nos vamos\n\nEnvia un regalo usando el siguiente comando !shop <regalo>, todo a 5 huachis.\n\nRegalo | Comando\n:--|--:\nMonas Chinas | monachina\n\nCompleta tu compra de la siguiente manera:\n\n    shop comando\n\n    Ejemplo: shop monachina\n\n    (no olvides el signo de exclamación)\n\nNo respondas a este comentario.")

                        elif opcion == "monachina":

                            compra = shop(str(comment.author),str(comment.parent().author),'monachina')

                            print(f'----\n{compra}')

                            comment.reply(compra)
   
                    except:
                        #Enviar mensaje de error si el empleado no entendio lo que recibio
                        comment.reply(random.choice(resp_empleado_error))

                
                elif "!asalto" in comment.body:

                    #Realizar consulta
                    try:

                        asalto = tumbar(str(comment.author),str(comment.parent().author))

                        print(f'----\n{asalto}')

                        #Responder al cliente
                        comment.reply(asalto)

                    except:
                        #Enviar mensaje de error si el empleado no entendio lo que recibio
                        comment.reply(random.choice(resp_empleado_error))
                        
def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    unread_messages = []

    for mensaje in reddit.inbox.unread(limit=None):

        print(f'----\nEnviando estado de cuenta para: {mensaje.author}')

        try:
            if "!historial" in mensaje.body:

                estado_cuenta = historial(str(mensaje.author))

                mensaje.reply(f"Estado de Cuenta: {mensaje.author}\n\nSaldo: {estado_cuenta[1]} Huachicoin(s)\n\nCantidad de Depositos: {len(estado_cuenta[2])}\n\nCantidad de Retiros: {len(estado_cuenta[3])}")

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
            

            elif "!saldo" in mensaje.body or "!saldazo" in mensaje.body:

                consulta = saldazo(str(mensaje.author))

                mensaje.reply(consulta)
            
        except:

            mensaje.reply(random.choice(resp_tip_cuenta))
            
        #Preparar para marcar como leido
        unread_messages.append(mensaje)

    reddit.inbox.mark_read(unread_messages)

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

                reddit.redditor(destinatario).message("Te han enviado un regalito.....",f"{remitente} te ha enviado una mona china! Kawaii desu ne! \n\n [Mona China]({monachina})")

                return random.choice(resp_shop)

def tumbar(cholo,victima):
    """Saca 5 varos morro"""

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
            if Huachis.saldo_total < 5:

                return "Chale, asaltaste a alguien sin dinero, mal pedo."
            
            else:

                if Huachis.Verificar_Usuario(cholo) == False:
                    #Abrimos cuenta y le damos dineros de bienvenida
                    Huachis.Bono_Bienvenida(cholo)
                
                    reddit.redditor(cholo).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el post sticky en Mujico para mas informacion de como usar la red.\n\nAqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: \n\n!historial o !saldo / !saldazo")
                
                #Enviar Binero
                Huachis.Enviar_Bineros(cholo,5)

                return random.choice(resp_tumbar_cholo) + "\n\n__Ganaste 5 Huachicoins__"

    else:
        #Acceder a la HuachiNet
        Huachis = HuachiNet(cholo)

        #Primero verificar que el remitente tenga una cuenta
        if Huachis.Verificar_Usuario(cholo) == False:
        
            return random.choice(resp_tip_cuenta)

        else:
            #Verificar que se tenga saldo suficiente para la transaccion
            if Huachis.saldo_total < 5:

                return "Perdiste, pero no tienes dinero que dar."
            
            else:
                #Enviar Binero
                Huachis.Enviar_Bineros(victima,5)

                return random.choice(resp_tumbar_victima) + "\n\n__Perdiste 5 Huachicoins__"


if __name__ == "__main__":
    
    empleado_del_mes()

    print("\nTransacciones al corriente señor!")

    servicio_al_cliente()

    print("\nYa respondi a todas las quejas patron!")




