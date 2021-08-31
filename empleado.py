# This Python file uses the following encoding: utf-8
from core import *
import concurrent.futures
import traceback

cirilo = Empleado_del_mes()

tareas = {"!tip" : cirilo.propina,
          "!saldo" : cirilo.saldazo,
          "!saldazo": cirilo.saldazo,
          "!rankme" : cirilo.rankme,
          "!rank25" : cirilo.rank25,
          "!rank" : cirilo.rank,
          "!shop" : cirilo.Shop,
          "!huachibono" : cirilo.huachibonos,
          "!guild" : cirilo.guild,
          "!build" : cirilo.build,
          "!asalto" : cirilo.asaltos,
          "!atraco" : cirilo.asaltos,
          "!levanton" : cirilo.levanton,
          "!huachito" : cirilo.huachito,
          "!poker" : cirilo.poker,
          "!huachilate" : cirilo.huachilate,
          "!huachilote" : cirilo.huachilate,
          "!rtd" : cirilo.rollthedice,
          "!portafolio" : cirilo.portafolio,
          "!stonks" : cirilo.stonks,
          "!comprar" : cirilo.comprar,
          "!vender" : cirilo.vender,
          "!long" : cirilo.comprar,
          "!short" : cirilo.vender,
          "!huachiswap" : cirilo.huachiswap,
          "!flair" : cirilo.flair
         }

def Jornada():
    """El motor de nuestra huachieconomia"""   

    movimientos = 0   

    #Cuidado con el futuro, es incierto.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:

        #Buscar subreddits
        for subreddit in config.SUBREDDITS:
        
            for comment in reddit.subreddit(subreddit).comments(limit=30):

                if comment.parent().author != None and comment.parent().author != "None":

                    #Buscar si el comentario ha sido procesado previamante
                    if cirilo.buscar_log(id) == False:

                        texto = str(comment.body).lower()

                        comandos = cirilo.comandos(texto)

                        if comandos == None:

                            continue

                        else:

                            #Agregar comentario al log
                            cirilo.actualizar_log(id)

                            remitente = str(comment.author)

                            destinatario = str(comment.parent().author)

                            id = str(comment.id)

                            for comando in comandos:
                            
                                if comando in ["!tip","!shop","!huachiswap"]:

                                    executor.submit(tareas[comando],texto,remitente,destinatario,id)
                        
                                    movimientos += 1

                                if comando in ["!huachibono","!guild","!huachito","!huachilate","!huachilote","!rtd","!long","!short","!comprar","!vender"]:
                                
                                    executor.submit(tareas[comando],texto,remitente,id)

                                    movimientos += 1

                                if comando in ["!saldo","!saldazo","!rank","!rankme","!rank25","!build","!portafolio","!stonks"]:
                                
                                    executor.submit(tareas[comando],remitente,id)

                                    movimientos += 1

                                if comando in ["!asalto","!atraco","!levanton"]:

                                    if comando == "!levanton":

                                        executor.submit(tareas[comando],texto,remitente,id)

                                        movimientos += 1

                                    else:
                                    
                                        tipo = comando.replace("!","").strip()

                                        executor.submit(tareas[comando],remitente,destinatario,tipo,id)

                                        movimientos += 1

                                if comando == "!poker":

                                    executor.submit(tareas[comando],remitente,destinatario,id)

                                    movimientos += 1
                                
                                if comando == "!flair":
                                
                                    executor.submit(tareas[comando],str(comment.body),remitente,id)

                                    movimientos += 1

        return movimientos

                    
def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    for mensaje in reddit.inbox.unread(limit=100):

        if mensaje.author in prohibido:
            pass

        #Buscar si el mensaje ha sido procesado previamante
        if cirilo.buscar_log(str(mensaje.id)) == False:

            try:

                if "!historial" in mensaje.body:

                    #Agregar mensaje al log
                    cirilo.actualizar_log(str(mensaje.id))

                    print(f'Enviando estado de cuenta: {mensaje.author}')

                    huachis = HuachiNet(str(mensaje.author))

                    asalto_victoria = [item for item in huachis.asaltos if int(item[2]) > 0]

                    asalto_perdida = [item for item in huachis.asaltos if int(item[2]) < 0]

                    atraco_victoria = [item for item in huachis.atracos if int(item[2]) > 0]

                    atraco_perdida = [item for item in huachis.atracos if int(item[2]) < 0] 

                    chunk = f"__Saldo: {huachis.saldo_total} Huachicoin(s)__\n\n**Total de movimientos**\n\nDepositos: {len(huachis.depositos)}  |  Retiros: {len(huachis.retiros)}\n\nAsaltos | ganados: {len(asalto_victoria)} | perdidos: {len(asalto_perdida)}\n\nAtracos | ganados: {len(atraco_victoria)} | perdidos: {len(atraco_perdida)}\n\nHuachitos | Comprados: {len(huachis.huachitos)} | Ganados: {len(huachis.premios_huachito)}\n\nBuild: �{huachis.perk} (energia disponible: {huachis.power})  |  �{huachis.trait}  |  ⚔️{huachis.weapon}\n\nFecha | Nota | Cantidad | Destino / Origen\n:--|:--:|--:|:--:\n"

                    for i,item in enumerate(huachis.historial,start=1):

                        chunk += f"{datetime.fromtimestamp(float(item[1])).ctime()} | {item[3]} | {item[2]} | {item[4]}\n"
                        
                        if len(huachis.historial) < 20:
                            
                            x = len(huachis.historial)

                        else:

                            x = 20
                            
                        if i % x == 0:

                            reddit.redditor(str(mensaje.author)).message(f"Estado de Cuenta: {mensaje.author}",chunk)

                            break
                
            except:

                #Enviar mensaje de error si el empleado no entendio lo que recibio
                cirilo.error_log(f"HuachiSwap - Usuario {str(mensaje.author)} - Comentario {str(mensaje.id)}" + traceback.format_exc())

                mensaje.reply(random.choice(resp_empleado_error))


if __name__ == "__main__":
    
    while True:

        start_time = time.time()

        movs = Jornada()

        servicio_al_cliente()

        print("\nTermine mi trabajo patron!")

        stats = f"--- {time.time() - start_time} seconds --- Movimientos: ({movs})"

        print(stats)

        with open("./timelog.txt","a",encoding="utf-8") as file:

            file.write(stats + "\n")

        time.sleep(30)
        
    
    
