from core import HuachiNet
import praw
import config
import sqlite3
import datetime
import random

conn_log = sqlite3.connect("boveda.sqlite3")

resp_saldo = ["Tu saldo es:", "Se me perdio tu cartera......no te creas:","Gusta redondear los centavos?:","Creo que una de tus monedas es falsa: ", "Puntos de Soriana"]

resp_tip_envio = ["Mandaste tus huachicoins papu! sin pagar comision.",
                  "Listo, joven.",
                  "Ojala a mi me pagaran esa cantidad",
                  "Enviando werito",
                  "Esta un poco lento el sistema, pero si jalo con el cliente anterior"]

resp_empleado_error = ["No lo se, no te entendi! Borra esto e intentalo de nuevo.",
                       "No me hagas preguntas complejas, apenas termine la secundaria",
                       "Mira, ya te dije que eso no lo tenemos aqui",
                       "En la otra caja le cobran wero",
                       "Se cayo el sistema joven",
                       "Tu orden me trabo los momos, mi patron se va a enojar"]

resp_tip_cuenta = ["Hubo un error, espera, no tienes cuenta en HuachiNet!",
                   "Mira rey, sin cuenta, no hay movimientos",
                   "Aber calmese señora, ya le dije que no la tenemos en el sistema",
                   "Maricanuebo sin cuenta en HuachiNet"]

resp_tip_sinbineros = ["Ya se te acabo el credito",
                       "Mas bien me vas a terminar debiendo, depositale mas a tu cuenta.",
                       "Pongase a jalar, que se ocupan mas huachicoins",
                       "Pide lismona para completa la transaccion",
                       "Ni con los puntos del soriana alcanzas a completa el monto",
                       "Hijole, no puedo ayudarte a completar la cantidad"]

resp_tip_empleado = ["Oye! Muchas gracias!, mi salario es basura!",
                     "Gracias, una paso mas a la dignidad, que la vida tanto me ha robado!",
                     "Awebo, ya salio para la cagua!",
                     "Te pusiste guap@, la proxima el vikingo va por mi cuenta! te dejo ponerle queso gratis, nomas una apachurrada porque luego mi jefe se da cuenta.",
                     "No esperaba esto, bueno si, mi trabajo es poco, pero es honesto.",
                     "Si se te pega otra monedita por ahi, no me awito"]

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
        
        return "Hubo un problema, no perteneces a la HuachiNet, ubicate niñ@!"

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
            #Verificar si el destinatario existe en la HuachiNet
            if Huachis.Verificar_Usuario(destinatario) == False:
                #Abrimos cuenta y le damos dineros de bienvenida
                Huachis.Bono_Bienvenida(destinatario)
            
            #Iniciamos transaccion
            Huachis.Enviar_Bineros(destinatario,cantidad)

            if destinatario == "Empleado_del_mes":

                return random.choice(resp_tip_empleado) + f" ({cantidad} Huachicoins)"

            else:

                return random.choice(resp_tip_envio) + f" ({cantidad} Huachicoins)"

def historial(redditor_id) -> list:
    """Revisar el historial de movimientos del cliente"""

    Huachis = HuachiNet(redditor_id)

    #Primero verificar que el remitente tenga una cuenta
    if Huachis.Verificar_Usuario(redditor_id) == False:
        
        return "Dafuq, no perteneces a la HuachiNet, Ubicate Niñ@!"

    else:

        return (Huachis.historial,Huachis.saldo_total,Huachis.depositos,Huachis.retiros)

def empleado_del_mes():
    """El motor de nuestra huachieconomia"""

    reddit = praw.Reddit(client_id=config.APP_ID, client_secret=config.APP_SECRET,
                         user_agent=config.USER_AGENT, username=config.REDDIT_USERNAME,
                         password=config.REDDIT_PASSWORD)        

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

                            #Actualizar log unicamente en mensaje exitoso
                            actualizar_log(str(comment.id))
                            
                            #Responder al cliente
                            comment.reply(transaccion)
                        
                        except:
                            #Enviar mensaje de error si el empleado no entendio lo que recibio
                            comment.reply(random.choice(resp_empleado_error))

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

def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    reddit = praw.Reddit(client_id=config.APP_ID, client_secret=config.APP_SECRET,
                             user_agent=config.USER_AGENT, username=config.REDDIT_USERNAME,
                             password=config.REDDIT_PASSWORD) 

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
            
        #Preparar para marcar como leido
        unread_messages.append(mensaje)

    reddit.inbox.mark_read(unread_messages)


if __name__ == "__main__":

    empleado_del_mes()

    print("\nTransacciones al corriente señor!")

    servicio_al_cliente()

    print("\nYa respondi a todas las quejas patron!")



