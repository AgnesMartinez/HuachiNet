# This Python file uses the following encoding: utf-8
from core import *
#import concurrent.futures
import traceback

cirilo = Empleado_del_mes()

tareas = {"!tip": cirilo.propina,
          "!saldo": cirilo.saldazo,
          "!saldazo": cirilo.saldazo,
          "!rankme": cirilo.rankme,
          "!rank25": cirilo.rank25,
          "!rank": cirilo.rank,
          "!shop": cirilo.Shop,
          "!huachibono": cirilo.huachibonos,
          "!guild": cirilo.guild,
          "!build": cirilo.build,
          "!asalto": cirilo.asaltos,
          "!atraco": cirilo.asaltos,
          "!levanton": cirilo.levanton,
          "!huachito": cirilo.huachito,
          "!poker": cirilo.poker,
          "!huachilate": cirilo.huachilate,
          "!huachilote": cirilo.huachilate,
          "!rtd": cirilo.rollthedice,
          "!deposito": cirilo.deposito,
          "!retiro": cirilo.retiro,
          "!flair": cirilo.flair
          }


def Jornada():
    """El motor de nuestra huachieconomia"""

    # Cuidado con el futuro, es incierto.

    #Los tiempos de cirilo son perfectos
    tiempos = open("./timelog.txt", "a", encoding="utf-8")

    # Buscar subreddits
    for subreddit in config.SUBREDDITS:

        for comment in reddit.subreddit(subreddit).comments(limit=50):

            if comment.parent().author != None and comment.parent().author != "None":

                id = str(comment.id)

                # Buscar si el comentario ha sido procesado previamante
                if cirilo.buscar_log(id) == False:

                    texto = str(comment.body).lower()

                    comandos = cirilo.comandos(texto)

                    if comandos == None or comandos == []:

                        continue

                    else:

                        # Agregar comentario al log
                        cirilo.actualizar_log(id)

                        remitente = str(comment.author)

                        destinatario = str(comment.parent().author)

                        for i,comando in enumerate(comandos):

                            if i == 2:
                                
                                break

                            if comando in ["!tip", "!shop"]:

                                start = time.time()

                                tareas[comando](texto, remitente, destinatario, id)

                                tiempos.write(f"{comando} --- {time.time() - start} segundos" + "\n")

                            if comando in ["!huachibono", "!guild", "!huachito", "!huachilate", "!huachilote", "!rtd", "!deposito", "!retiro"]:

                                start = time.time()

                                tareas[comando](texto, remitente, id)

                                tiempos.write(f"{comando} --- {time.time() - start} segundos" + "\n")

                            if comando in ["!saldo", "!saldazo", "!rank", "!rankme", "!rank25", "!build"]:

                                start = time.time()

                                tareas[comando](remitente, id)

                                tiempos.write(f"{comando} --- {time.time() - start} segundos" + "\n")

                            if comando in ["!asalto", "!atraco", "!levanton"]:

                                start = time.time()

                                if comando == "!levanton":

                                    tareas[comando](texto, remitente, id)

                                    tiempos.write(f"{comando} --- {time.time() - start} segundos" + "\n")

                                else:

                                    tipo = comando.replace("!", "").strip()

                                    tareas[comando](remitente, destinatario, tipo, id)

                                    tiempos.write(f"{comando} --- {time.time() - start} segundos" + "\n")

                            if comando == "!poker":

                                start = time.time()

                                tareas[comando](remitente, destinatario, id)

                                tiempos.write(f"{comando} --- {time.time() - start} segundos" + "\n")

                            if comando == "!flair":

                                start = time.time()

                                tareas[comando](str(comment.body), remitente, id)

                                tiempos.write(f"{comando} --- {time.time() - start} segundos" + "\n")

    tiempos.close()


def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    for mensaje in reddit.inbox.unread(limit=100):

        if mensaje.author in prohibido:
            pass

        # Buscar si el mensaje ha sido procesado previamante
        if cirilo.buscar_log(str(mensaje.id)) == False:

            try:

                if "!historial" in mensaje.body:

                    # Agregar mensaje al log
                    cirilo.actualizar_log(str(mensaje.id))

                    print(f'Enviando estado de cuenta: {mensaje.author}')

                    huachis = HuachiNet(str(mensaje.author))

                    asalto_victoria = [
                        item for item in huachis.asaltos if int(item[2]) > 0]

                    asalto_perdida = [
                        item for item in huachis.asaltos if int(item[2]) < 0]

                    atraco_victoria = [
                        item for item in huachis.atracos if int(item[2]) > 0]

                    atraco_perdida = [
                        item for item in huachis.atracos if int(item[2]) < 0]

                    chunk = f"__Cartera Principal: {huachis.saldo_total} huachicoin(s)__\n\n__Cuenta Bancadenas: {huachis.saldo_bancadenas} huachicoin(s)__\n\n**Transacciones**\n\nDepositos: {len(huachis.depositos)}  |  Retiros: {len(huachis.retiros)}\n\nAsaltos | ganados: {len(asalto_victoria)} | perdidos: {len(asalto_perdida)}\n\nAtracos | ganados: {len(atraco_victoria)} | perdidos: {len(atraco_perdida)}\n\nHuachitos | Comprados: {len(huachis.huachitos)} | Ganados: {len(huachis.premios_huachito)}\n\nBuild: �{huachis.perk} (energia disponible: {huachis.power})  |  �{huachis.trait}  |  ⚔️{huachis.weapon}\n\nFecha | Nota | Cantidad | Destino / Origen\n:--|:--:|--:|:--:\n"

                    for i, item in enumerate(huachis.historial, start=1):

                        chunk += f"{datetime.fromtimestamp(float(item[1])).ctime()} | {item[3]} | {item[2]} | {item[4]}\n"

                        if len(huachis.historial) < 20:

                            x = len(huachis.historial)

                        else:

                            x = 20

                        if i % x == 0:

                            reddit.redditor(str(mensaje.author)).message(
                                f"Estado de Cuenta: {mensaje.author}", chunk)

                            break

            except:

                # Enviar mensaje de error si el empleado no entendio lo que recibio
                cirilo.error_log(
                    f"HuachiSwap - Usuario {str(mensaje.author)} - Comentario {str(mensaje.id)}" + traceback.format_exc())

                mensaje.reply(random.choice(resp_empleado_error))


if __name__ == "__main__":

    while True:

        start_time = time.time()

        movs = Jornada()

        servicio_al_cliente()

        print("\nTermine mi trabajo patron!")

        stats = f"--- {time.time() - start_time} seconds"

        print(stats)

        time.sleep(60)
