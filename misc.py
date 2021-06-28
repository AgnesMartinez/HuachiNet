diccionario = {
  'stonks' : ("AAPL","AMZN","TSLA","MRNA","NFLX","NVDA","NIO","WMT","COST","TUP","GME","NTDOY","SNE","MSFT","INTC","AMD","BTC-USD","ETH-USD","LTC-USD","VET-USD","NANO-USD","DOGE-USD"),

  'mocoso miado' : "El usuario al que quieres enviar no tiene la madurez suficiente para entrar al sistema, es un pinche mocoso miado, dejalo ahi.",

  'opciones shop' : ("monachina","trapo","furro","nalgotica","cura","corvido","galleta","huachito","chambeadora","valentin"),
  
  'menu shop' : ("Menu Shop","__HuachiStore - Abierto cuando llegamos, cerrado cuando nos vamos__\n\nEnvia un regalo usando el comando shop, seguido de una opcion del menu, todo a 5 huachis.\n\nRegalo | subcomando\n:--|--:\nMonas Chinas | monachina\nTrapitos | trapo\nFurros | furro\nHuachito | huachito\nNalgoticas | nalgotica\nMDLP | cura / corvido\nGanosas (Revistas para adultos) | chambeadora\nGalleta de la fortuna | galleta\n\nCompleta tu compra de la siguiente manera:\n\n    shop comando\n\n    Ejemplo: shop monachina\n\n    (no olvides el signo de exclamación)\n\nUsalo en la seccion de comentarios."),

  'menu bonos' : ("Menu Huachibonos","__Huachibonos - Esta clase de bonos, no los tiene ni obama__\n\nRecuerda que los huachibonos � consumen enerrga! Para recargar tu huachibono � necesitas comprar uno nuevo. La energia no es acumulable.\n\nCosto pororuachibono: � = 1000  � = 500  ⚔️ = 250\n\nHuachibono | subcomando\n:--|--:\nBarrera Susana Distancia �  �susana\nJelatina de BANANA � | jelatina\nSeguro para la 3era edad � | seguro\nEstampita Detente � | d�te te\nMariguana roja � | roja\nMariguana azul � | azul\nMariguana dorada � | dorada\nChocomilk >� | choco>� | chocomilk\nCarta Blanca � | caguama\nEmulsion Scotch � | vitaminas\nMariguana verde � | verde\nPlatano ⚔️ | platano\nFlorecita de vive sin drogas ⚔️ | florecita\nRata con thinner ⚔️ | noroña\nFusca ⚔️ | fusca\nEcayecelosico ⚔️ | ecayece\n\nCompleta tu compra de la siguiente manera:\n\n    huachibono subcomando\n\n    Ejemplo: huachibono caguama\n\n    (no olvides el signo de exclamación)\n\nUsalo en la seccion de comentarios."),
  #huachibonos
  'bonos perks' : {"susana" : "Barrera Susana Distancia", "jelatina" : "Jelatina de BANANA", "seguro" : "Seguro para la 3era edad", "detente" : "Estampita Detente", "roja" : "Mariguana roja" , "azul" : "Mariguana azul", "dorada" : "Mariguana dorada"},

  'bonos traits' : {"chocomilk" : "Chocomilk", "caguama" : "Carta Blanca", "vitaminas" : "Emulsion Scotch", "mod" : "Marika","verde":"Mariguana verde"},

  'bonos weapons' : {"platano" : "Platano", "florecita" : "Florecita de vive sin drogas", "noroña" : "Rata con thinner", "fusca" : "Fusca", "ecayece" : "Ecayecelocico"},

  'bonos opciones' : ["susana","jelatina","seguro","detente","chocomilk","caguama","vitaminas","mod","platano","florecita","noroña","fusca","ecayece","verde","roja","azul","dorada"],
  
  'trait marika' : "Que es ese olor, __sniff sniff__ huele a que alguien compro el huachibono de 'mArIKa'. Salio mod y no quiere que lo roben, pero tampoco puede robar.",

  'trait vacuna' : "Esta persona ha sido inyectada con Patria! la vacuna mujicana, los efectos secundarios la volvieron inmune a los robos, dejame decirte que ya valiste madre F",

  'trait seguro' : "Esta cuenta tiene seguro activo contra maricanuebos, esperate a que se le acabe la vigencia para poderlo robar",

  'trait susana' : "Esta cuenta tiene la proteccion de susana distancia! Espera a que se le termine el efecto.",

  'respuestas bomba' : ["Como en buscaminas, te explotaron las bombas, perdiste!","Varias bombas werito, perdiste","BOMBA! mala suerte :'(","Te salio el negrito y el prietito del arroz, perdistes."],

  'respuestas perdida' : ["Sigue participando","Suerte para la proxima","Asi es el negocio de rascar boletitos, llevate un dulce del mostrador","Ni pepsi carnal", "Asi pasa cuando sucede","No te awites niño chillon"],

  'respuesta dados' : ["Suerte para la proxima","No estan cargados, te lo juro","Sigue participando","Hoy no es tu dia","No te awites, niño chillon"]
}

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

resp_huachilate = open("./frases/frases_huachilate.txt", "r", encoding="utf-8").read().splitlines()

resp_huachibono = open("./frases/frases_huachibono.txt", "r", encoding="utf-8").read().splitlines()

resp_huachiswap = open("./frases/frases_huachiswap.txt","r",encoding="utf-8").read().splitlines()

monaschinas = open("./shop/monaschinas.txt", "r", encoding="utf-8").read().splitlines()

trapos = open("./shop/trapos.txt", "r", encoding="utf-8").read().splitlines()

furros = open("./shop/furro.txt", "r", encoding="utf-8").read().splitlines()

nalgoticas = open("./shop/nalgoticas.txt", "r", encoding="utf-8").read().splitlines()

curas = open("./shop/curas.txt", "r", encoding="utf-8").read().splitlines()

chambeadoras = open("./shop/ganosas.txt", "r", encoding="utf-8").read().splitlines()

galletas = open("./shop/galletas.txt", "r", encoding="utf-8").read().splitlines()

valentines = open("./shop/valentin.txt", "r", encoding="utf-8").read().splitlines()

viejos = open("./shop/viejos_sabrozos.txt", "r", encoding="utf-8").read().splitlines()

emojis = ['👻','🐷','🐧','🦝','🍮', '💣','👾','👽','🦖','🥓','🤖']

premios_huachito = {}
premios_huachito['👻👻👻'] = 100
premios_huachito['👻👻👻👻'] = 900
premios_huachito['👻👻👻👻👻'] = 5000
premios_huachito['🦖🦖🦖'] = 90
premios_huachito['🦖🦖🦖🦖'] = 800
premios_huachito['🦖🦖🦖🦖🦖'] = 4500
premios_huachito['🦝🦝🦝'] = 80
premios_huachito['🦝🦝🦝🦝'] = 700
premios_huachito['🦝🦝🦝🦝🦝'] = 4000
premios_huachito['🍮🍮🍮'] = 70
premios_huachito['🍮🍮🍮🍮'] = 600
premios_huachito['🍮🍮🍮🍮🍮'] = 3500
premios_huachito['👾👾👾'] = 60
premios_huachito['👾👾👾👾'] = 500
premios_huachito['👾👾👾👾👾'] = 3000
premios_huachito['🐷🐷🐷'] = 50
premios_huachito['🐷🐷🐷🐷'] = 400
premios_huachito['🐷🐷🐷🐷🐷'] = 2500
premios_huachito['🐧🐧🐧'] = 40
premios_huachito['🐧🐧🐧🐧'] = 300
premios_huachito['🐧🐧🐧🐧🐧'] = 2000
premios_huachito['👽👽👽'] = 30
premios_huachito['👽👽👽👽'] = 200
premios_huachito['👽👽👽👽👽'] = 1500
premios_huachito['🤖🤖🤖'] = 20
premios_huachito['🤖🤖🤖🤖'] = 100
premios_huachito['🤖🤖🤖🤖🤖'] = 1500
premios_huachito['🥓🥓🥓🥓🥓'] = 10000


perks = {"Normal":(0,0,0,0),"Barrera Susana Distancia":(0,0,0,5),"Jelatina de BANANA":(20,0,0,5),"Seguro para la 3era edad":(0,0,0,5),"Estampita Detente":(30,0,30,5),"Mariguana roja": (50,-20,0,5),"Mariguana azul": (random.randint(20,50),valor,10,5),"Mariguana dorada": (69,0,30,5)}

traits = {"Normal":(0,0,0),"Chocomilk": (10,20,0),"Carta Blanca":(0,50,0),"Emulsion Scotch":(20,0,0),"Marika":(0,0,0),"Mariguana verde":(20,10,10),"Salchichas con anticongelante":(0,0,30),"Peste":(0,0,0),"Recargando":(0,0,0),"Vacuna": (80,20,0)}

weapons = {"Navaja":(0,0,0),"Platano":(random.randint(10,50),0,0),"Florecita de vive sin drogas":(30,0,0),"Rata con thinner":(0,25,0),"Fusca":(20,0,backfire),"Ecayecelocico":(20,0,10)}
