from core import HuachiNet
import praw
import config
import sqlite3
import datetime
import random

conn_log = sqlite3.connect("boveda.sqlite3")

resp_saldo = open("frases_saldo.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_envio = open("frases_envio.txt", "r", encoding="utf-8").read().splitlines()

resp_empleado_error = open("frases_error.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_cuenta = open("frases_cuenta.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_sinbineros = open("frases_sinbineros.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_empleado = open("frases_empleado.txt", "r", encoding="utf-8").read().splitlines()

reddit = praw.Reddit(client_id=config.APP_ID, client_secret=config.APP_SECRET,
                             user_agent=config.USER_AGENT, username=config.REDDIT_USERNAME,
                             password=config.REDDIT_PASSWORD) 

def buscar_log(comment_id):
    """Buscar si el comentario ha sido previamente procesado por el empleado del mes"""

    cursor = conn_log.cursor()

    query = """SELECT * FROM comentarios WHERE id_comment=?"""

    resultado = cursor.execute(query,(comment_id,)).fetchall()

    if resultado != []:
        for item in resultado:
            if comment_id in item[1]:
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
        return random.choice(resp_saldo) + f" {Huachis.saldo_total} Huachicoins"

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

            return random.choice(resp_tip_sinbineros) + f" ({cantidad} Huachicoins)"

        else:
            #calcula la edad del destinatario para evitar spam de cuentas recien creadas
            cuenta_dias = edad_cuenta(destinatario)

            if cuenta_dias < 28:

                return "La cuenta a la que quieres enviar no tiene la madurez suficiente para entrar al sistema, es un pinche mocoso miado, dejalo ahi."

            else:
                #Verificar si el destinatario existe en la HuachiNet
                if Huachis.Verificar_Usuario(destinatario) == False:
                    #Abrimos cuenta y le damos dineros de bienvenida
                    Huachis.Bono_Bienvenida(destinatario)
                
                    reddit.redditor(destinatario).message("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el post sticky en Techo Negro para mas informacion de como usarse, proximamente podrias usar tus huachicoins en mujico, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial o !saldo / !saldazo")
            
                #Iniciamos transaccion
                Huachis.Enviar_Bineros(destinatario,cantidad)

                if destinatario == "Empleado_del_mes":

                    return random.choice(resp_tip_empleado) + f" ({cantidad} Huachicoins)"

                else:
                
                    return random.choice(resp_tip_envio) + f" ({cantidad} Huachicoins)"

def edad_cuenta(redditor_id) -> int:
    """calcular la edad en dias de la cuenta"""

    timestamp_usuario =  reddit.redditor(redditor_id)
    
    f_cuenta = datetime.fromtimestamp(timestamp_usuario.created_utc)

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

def empleado_del_mes():
    """El motor de nuestra huachieconomia"""       

    #Buscar subreddits
    for subreddit in config.SUBREDDITS:
        #Buscar Publicaciones
        for submission in reddit.subreddit(subreddit).new(limit=30):
            #Buscar comentarios
            for comment in submission.comments.list():
                #Buscar comandos
                if "!tip" in comment.body:

                    #Verificar si el comentario ya fue procesado
                    if buscar_log(str(comment.id)) == True:
                        pass
                    
                    else:
                        #Realizar transaccion
                        try:
                            string = str(comment.body)
                
                            start = string.index("!tip")

                            cantidad = int(string[start:].replace("!tip","").strip())

                            transaccion = tip(str(comment.author),str(comment.parent().author),abs(cantidad))

                            print(f'----\n{transaccion}')

                            #Actualizar log
                            actualizar_log(str(comment.id))
                            
                            #Responder al cliente
                            comment.reply(transaccion)

                        
                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                            #Actualizar el log
                            actualizar_log(str(comment.id))

                elif "!saldo" in comment.body or "!saldazo" in comment.body:

                    #Verificar si el comentario ya fue procesado
                    if buscar_log(str(comment.id)) == True:
                        pass
                    
                    else:
                        #Realizar consulta
                        try:
                        
                            consulta = saldazo(str(comment.author))

                            print(f'----\n{consulta}')

                            #Actualizar log unicamente en mensaje exitoso
                            actualizar_log(str(comment.id))
                            
                            #Responder al cliente
                            comment.reply(consulta)
                        
                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))
                            #Actualizar el log
                            actualizar_log(str(comment.id))

def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    unread_messages = []

    for mensaje in reddit.inbox.unread(limit=None):

        print(f'----\nEnviando estado de cuenta para: {mensaje.author}')

        if "!historial" in mensaje.body:

            estado_cuenta = historial(str(mensaje.author))

            mensaje.reply(f"Estado de Cuenta: {mensaje.author}  |  Saldo: {estado_cuenta[1]} Huachicoins     |  Cantidad de Depositos: {len(estado_cuenta[2])}  |  Cantidad de Retiros: {len(estado_cuenta[3])}")

            for item in estado_cuenta[0]:

                readable = datetime.datetime.fromtimestamp(float(item[1])).ctime()

                if "Retiro" in item:
                    mensaje.reply(f"ID:  {item[0]}  |  Timestamp: {readable}  |  Cantidad: {item[2]}  |  Movimiento: {item[3]}  |  Destino: {item[4]}")
                
                else:
                    mensaje.reply(f"ID:  {item[0]}  |  Timestamp: {readable} |  Cantidad: {item[2]} |  Movimiento: {item[3]}  |  Origen: {item[4]}")

        elif "!saldo" in mensaje.body or "!saldazo" in mensaje:

            consulta = saldazo(str(mensaje.author))

            mensaje.reply(consulta)
            
        #Preparar para marcar como leido
        unread_messages.append(mensaje)

    reddit.inbox.mark_read(unread_messages)


if __name__ == "__main__":
    
    empleado_del_mes()

    print("\nTransacciones al corriente señor!")

    servicio_al_cliente()

    print("\nYa respondi a todas las quejas patron!")



