
diccionario = {
  'stonks' : ("AAPL","AMZN","TSLA","MRNA","NFLX","NVDA","NIO","WMT","COST","TUP","GME","NTDOY","SNE","MSFT","INTC","AMD","BTC-USD","ETH-USD","LTC-USD","VET-USD","NANO-USD","DOGE-USD"),

  'opciones shop' : ("monachina","trapo","furro","nalgotica","cura","corvido","galleta","huachito","chambeadora","valentin"),
  
  'menu shop' : ("Menu Shop","__HuachiStore - Abierto cuando llegamos, cerrado cuando nos vamos__\n\nEnvia un regalo usando el comando shop, seguido de una opcion del menu, todo a 5 huachis.\n\nRegalo | subcomando\n:--|--:\nMonas Chinas | monachina\nTrapitos | trapo\nFurros | furro\nHuachito | huachito\nNalgoticas | nalgotica\nMDLP | cura / corvido\nGanosas (Revistas para adultos) | chambeadora\nGalleta de la fortuna | galleta\n\nCompleta tu compra de la siguiente manera:\n\n    shop comando\n\n    Ejemplo: shop monachina\n\n    (no olvides el signo de exclamación)\n\nUsalo en la seccion de comentarios."),

  'menu bonos' : ("Menu Huachibonos","__Huachibonos - Esta clase de bonos, no los tiene ni obama__\n\nRecuerda que los huachibonos � consumen enerrga! Para recargar tu huachibono � necesitas comprar uno nuevo. La energia no es acumulable.\n\nCosto pororuachibono: � = 1000  � = 500  ⚔️ = 250\n\nHuachibono | subcomando\n:--|--:\nBarrera Susana Distancia �  �susana\nJelatina de BANANA � | jelatina\nSeguro para la 3era edad � | seguro\nEstampita Detente � | d�te te\nMariguana roja � | roja\nMariguana azul � | azul\nMariguana dorada � | dorada\nChocomilk >� | choco>� | chocomilk\nCarta Blanca � | caguama\nEmulsion Scotch � | vitaminas\nMariguana verde � | verde\nPlatano ⚔️ | platano\nFlorecita de vive sin drogas ⚔️ | florecita\nRata con thinner ⚔️ | noroña\nFusca ⚔️ | fusca\nEcayecelosico ⚔️ | ecayece\n\nCompleta tu compra de la siguiente manera:\n\n    huachibono subcomando\n\n    Ejemplo: huachibono caguama\n\n    (no olvides el signo de exclamación)\n\nUsalo en la seccion de comentarios."),
  #huachibonos
  'bonos perks' : {"susana" : "Barrera Susana Distancia", "jelatina" : "Jelatina de BANANA", "seguro" : "Seguro para la 3era edad", "detente" : "Estampita Detente", "roja" : "Mariguana roja" , "azul" : "Mariguana azul", "dorada" : "Mariguana dorada"},

  'bonos traits' : {"chocomilk" : "Chocomilk", "caguama" : "Carta Blanca", "vitaminas" : "Emulsion Scotch", "mod" : "Marika","verde":"Mariguana verde"},

  'bonos weapons' : {"platano" : "Platano", "florecita" : "Florecita de vive sin drogas", "noroña" : "Rata con thinner", "fusca" : "Fusca", "ecayece" : "Ecayecelocico"},

  'bonos opciones' : ["susana","jelatina","seguro","detente","chocomilk","caguama","vitaminas","mod","platano","florecita","noroña","fusca","ecayece","verde","roja","azul","dorada"]

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

