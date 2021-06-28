# This Python file uses the following encoding: utf-8
from habilidades import *


def empleado_del_mes():
    """El motor de nuestra huachieconomia"""      

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

                    if (comment.parent().author != None and comment.parent().author != "None") or (comment.author != None and comment.author != "None"):
                        comandos += 1


                        #Buscar comandos
                        if "!tip" in item:

                            try:
                                #Extraemos la cantidad
                                cantidad = (re.findall('!tip\ *(\d+)', texto))[0]

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
                                            
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Tip -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!saldazo" in item or "!saldo" in item:

                            #Realizar consulta
                            try:
                                
                                consulta = saldazo(str(comment.author))

                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("Saldazo",consulta)

                                
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Saldazo -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!rankme" in item:

                            #Realizar consulta
                            try:

                                rankme = rank(str(comment.author),0)

                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("Su lugar en la HuachiNet:",rankme)


                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("rankme -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!rank25" in item:
                          
                            #Realizar consulta
                            try:
                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("Forbes Mujico Top 25",
                                    rank(str(comment.author),25))


                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("rank25 -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!rank" in item:

                            #Realizar consulta
                            try:
                                #Responder al cliente
                                reddit.redditor(str(comment.author)).message("Forbes Mujico Top 10",
                                    rank(str(comment.author),10))


                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("rank10" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!shop" in item:

                            if comment.parent().author != None and comment.parent().author != "None":

                                comandos += 2

                                #Opciones del menu
                                opciones = diccionario['opciones shop']

                                if "menu" in texto:
                                        
                                    #Enviar menu
                                    reddit.redditor(str(comment.author)).message(diccionario['menu shop'])

                                    continue
                            
                                for opcion in opciones:

                                    if opcion in texto:
                                        
                                        #Enviar regalo
                                        shop_item(opcion)


                        elif "!huachibono" in item:

                            if comment.author != None and comment.author != "None":

                                comandos += 2

                                #huachibonos
                                perks = diccionario['bonos perks']

                                traits = diccionario['bonos traits']

                                weapons = diccionario['bonos weapons']

                                opciones = diccionario['opciones']


                                try:

                                    if "menu" in texto:
                                        
                                        #Enviar menu
                                        reddit.redditor(str(comment.author)).message(diccionario['menu bonos'])

                                    for opcion in opciones:
                                
                                        if opcion in texto:
                                        
                                            if opcion in perks:

                                                #comprar huachibono
                                                shop_huachibono("perk",perks[opcion])

                                            elif opcion in traits:

                                                #comprar huachibono
                                                shop_huachibono("trait",traits[opcion])

                                            elif opcion in weapons:

                                                #comprar huachibono
                                                shop_huachibono("weapon",weapons[opcion])


                                except:
                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    error_log("huachibono" + traceback.format_exc())

                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!asalto" in item:

                            #Realizar consulta
                            try:

                                resultado = asalto(str(comment.author),str(comment.parent().author),"asalto")

                                #Responder al cliente
                                comment.reply(resultado)

                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("Asalto -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!atraco" in item:
                           
                                #Realizar consulta
                                try:

                                    resultado = asalto(str(comment.author),str(comment.parent().author),"atraco")

                                    #Responder al cliente
                                    comment.reply(resultado)

                                except:
                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    error_log("Atraco -" + traceback.format_exc())

                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!levanton" in item:

                            if comment.parent().author != None and comment.parent().author != "None":

                                comandos += 2

                                #Realizar consulta
                                try:

                                    victima = buscar_usuario(texto)

                                    resultado = asalto(str(comment.author),victima,"levanton")

                                    #Responder al cliente
                                    comment.reply(resultado)

                                except:
                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    #error_log("Levanton -" + traceback.format_exc())

                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!huachito" in item:

                            if comment.author != None and comment.author != "None":

                                comandos += 2

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
                                    error_log("Huachito -" + traceback.format_exc())
                                    
                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!poker" in item:
                       
                                #Realizar consulta
                                try:

                                    resultado = pokermujicano(str(comment.author))

                                    #Responder al cliente
                                    comment.reply(resultado)


                                except:
                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    error_log("Poker -" + traceback.format_exc())
                                    
                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))



                        elif "!huachilate" in item or "!huachilote" in item:

                            if comment.author != None and comment.author != "None":

                                comandos += 2

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

                                            compra = huachilate(str(comment.author))

                                        #Responder al cliente
                                        reddit.redditor(str(comment.author)).message(f"Compraste {cantidad} huachilate(s)!",compra)


                                except:
                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    error_log("Huachilate -" + traceback.format_exc())
                                    
                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!rtd" in item:

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
                                            
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("RTD -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!stonks" in item:

                            if comment.author != None and comment.author != "None":

                                comandos += 2

                                try:
                                
                                    #Realizamos la consulta
                                    resultado = consultar_stonks()
                                        
                                    #Responder al cliente
                                    reddit.redditor(str(comment.author)).message("HuachiSwap Liquidity Pool",resultado)
            
                                                
                                except:
                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    error_log("stonks -" + traceback.format_exc())

                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!portafolio" in item:

                            if comment.author != None and comment.author != "None":

                                comandos += 2

                                try:
                                
                                    #Realizamos la consulta
                                    resultado = portafolio(str(comment.author))
                                        
                                    #Responder al cliente
                                    reddit.redditor(str(comment.author)).message("HuachiSwap - Portafolio",resultado)
                
                                                
                                except:
                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    error_log("Portafolio -" + traceback.format_exc())

                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))

                        
                        elif "!comprar" in item or "!long" in item:

                            if comment.author != None and comment.author != "None":

                                comandos += 2

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

                                            break
                                
                                except:

                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    error_log("Long -" + traceback.format_exc())
                                    
                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!vender" in item or "!short" in item:

                            if comment.author != None and comment.author != "None":

                                comandos += 2

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

                                            break
                                except:

                                    #Enviar mensaje de error si el empleado no entendio lo que recibio
                                    error_log("Short -" + traceback.format_exc())
                                    
                                    reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


                        elif "!huachiswap" in item:

                            if comment.author != None and comment.author != "None":

                                comandos += 2

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

                                        break             
                                            
                            except:
                                #Enviar mensaje de error si el empleado no entendio lo que recibio
                                error_log("HuachiSwap -" + traceback.format_exc())

                                reddit.redditor(str(comment.author)).message("Mensaje Error",random.choice(resp_empleado_error))


def servicio_al_cliente():
    """Responder a los papus y a las mamus sobre sus cuentas"""

    for mensaje in reddit.inbox.unread(limit=100):

        if mensaje.author in prohibido:
            pass

        #Buscar si el mensaje ha sido procesado previamante
        if buscar_log(str(mensaje.id)) == False:

            try:

                if "!historial" in mensaje.body:

                    #Agregar mensaje al log
                    actualizar_log(str(mensaje.id))

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
                
            except Exception as e:
                #Mensaje no tienes cuenta
                error_log(e)

                mensaje.reply(random.choice(resp_tip_cuenta))


if __name__ == "__main__":
    
    while True:

        start_time = time.time()

        empleado_del_mes()

        servicio_al_cliente()

        print("\nTermine mi trabajo patron!")

        print(f"--- {time.time() - start_time} seconds ---")  

        time.sleep(30)
