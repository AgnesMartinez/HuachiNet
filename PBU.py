from core import HuachiNet
import praw
import config

#Acceder a la HuachiNet de la bodega
Huachis_master = HuachiNet('Bodega')

usuarios = [item[0] for item in Huachis_master.Ranking()]

#Configuracion del cliente de reddit
reddit = praw.Reddit(client_id=config.APP_ID, 
                     client_secret=config.APP_SECRET,
                     user_agent=config.USER_AGENT, 
                     username=config.REDDIT_USERNAME,
                     password=config.REDDIT_PASSWORD) 

#Iterar por cada usuario
for usuario in usuarios:
    #Acceder a la cuenta del usuario
    Huachis_slave = HuachiNet(usuario)

    #Cantidad de transacciones
    transacciones = Huachis_slave.historial

    #Entregar bineros segun tabulador 
    #Pension basica (50 a 200 movimientos) = 50 huachicoins semanales
    #Pension intermedia (201 a 500 movimientos) = 60 huachicoins semanales
    #Pension avanzada (501 a 1000 movimientos) = 70 huachicoins semanales

    if len(transacciones) > 50 and len(transacciones) < 201:

        #Entregar pension basica
        Huachis_master.Enviar_Bineros(usuario,50,pension=True)

        reddit.redditor(usuario).message("Entrega de pension mujicana basica", "Se te han depositado 50 huachicoins a tu cuenta")

    elif len(transacciones) > 200 and len(transacciones) < 501:
        
        #Entregar pension basica
        Huachis_master.Enviar_Bineros(usuario,60,pension=True)

        reddit.redditor(usuario).message("Entrega de pension mujicana intermedia", "Se te han depositado 60 huachicoins a tu cuenta")

    elif len(transacciones) > 500:
        
        Entregar pension basica
        Huachis_master.Enviar_Bineros(usuario,70,pension=True)

        reddit.redditor(usuario).message("Entrega de pension mujicana avanzada", "Se te han depositado 70 huachicoins a tu cuenta")



    

    

    