diccionario = {
  'stonks' : ("AAPL","AMZN","TSLA","MRNA","NFLX","NVDA","NIO","WMT","COST","TUP","GME","NTDOY","SNE","MSFT","INTC","AMD","BTC-USD","ETH-USD","LTC-USD","VET-USD","NANO-USD","DOGE-USD"),

  'bienvenida' : ("Bienvenid@ a la HuachiNet!", "Recuerda que todo esto es por mera diversion, amor al arte digital. Revisa el [post sticky](https://www.reddit.com/r/Mujico/comments/ky9ehw/comandos_de_la_huachinet/) en Mujico para mas informacion de como usar la red, aqui mismo puedes consultar tu saldo e historial de tu cuenta, solo escribe: !historial"),
  
  'opciones shop' : ("monachina","trapo","furro","nalgotica","cura","corvido","galleta","huachito","chambeadora","valentin"),
  
  'menu shop' : ("Menu Shop","__HuachiStore - Abierto cuando llegamos, cerrado cuando nos vamos__\n\nEnvia un regalo usando el comando shop, seguido de una opcion del menu, todo a 5 huachis.\n\nRegalo | subcomando\n:--|--:\nMonas Chinas | monachina\nTrapitos | trapo\nFurros | furro\nHuachito | huachito\nNalgoticas | nalgotica\nMDLP | cura / corvido\nGanosas (Revistas para adultos) | chambeadora\nGalleta de la fortuna | galleta\n\nCompleta tu compra de la siguiente manera:\n\n    shop comando\n\n    Ejemplo: shop monachina\n\n    (no olvides el signo de exclamación)\n\nUsalo en la seccion de comentarios."),

  'menu bonos' : ("Menu Huachibonos","__Huachibonos - Esta clase de bonos, no los tiene ni obama__\n\nRecuerda que los huachibonos � consumen enerrga! Para recargar tu huachibono � necesitas comprar uno nuevo. La energia no es acumulable.\n\nCosto pororuachibono: � = 1000  � = 500  ⚔️ = 250\n\nHuachibono | subcomando\n:--|--:\nBarrera Susana Distancia �  �susana\nJelatina de BANANA � | jelatina\nSeguro para la 3era edad � | seguro\nEstampita Detente � | d�te te\nMariguana roja � | roja\nMariguana azul � | azul\nMariguana dorada � | dorada\nChocomilk >� | choco>� | chocomilk\nCarta Blanca � | caguama\nEmulsion Scotch � | vitaminas\nMariguana verde � | verde\nPlatano ⚔️ | platano\nFlorecita de vive sin drogas ⚔️ | florecita\nRata con thinner ⚔️ | noroña\nFusca ⚔️ | fusca\nEcayecelosico ⚔️ | ecayece\n\nCompleta tu compra de la siguiente manera:\n\n    huachibono subcomando\n\n    Ejemplo: huachibono caguama\n\n    (no olvides el signo de exclamación)\n\nUsalo en la seccion de comentarios."),
  #huachibonos
  'bonos perks' : {"susana" : "Barrera Susana Distancia", "jelatina" : "Jelatina de BANANA", "seguro" : "Seguro para la 3era edad", "detente" : "Estampita Detente", "roja" : "Mariguana roja" , "azul" : "Mariguana azul", "dorada" : "Mariguana dorada"},

  'bonos traits' : {"chocomilk" : "Chocomilk", "caguama" : "Carta Blanca", "vitaminas" : "Emulsion Scotch", "mod" : "Marika","verde":"Mariguana verde"},

  'bonos weapons' : {"platano" : "Platano", "florecita" : "Florecita de vive sin drogas", "noroña" : "Rata con thinner", "fusca" : "Fusca", "ecayece" : "Ecayecelocico"},

  'bonos opciones' : ["susana","jelatina","seguro","detente","chocomilk","caguama","vitaminas","mod","platano","florecita","noroña","fusca","ecayece","verde","roja","azul","dorada"],

  'chunk' : f"__Saldo: {estado_cuenta[1]} Huachicoin(s)__\n\n**Total de movimientos**\n\nDepositos: {len(estado_cuenta[2])}  /  Retiros: {len(estado_cuenta[3])}\n\nAsaltos ganados: {len(asalto_victoria)}  /  Asaltos perdidos: {len(asalto_perdida)}\n\nAtracos ganados: {len(atraco_victoria)}  /  Atracos perdidos: {len(atraco_perdida)}\n\nHuachitos Comprados: {len(estado_cuenta[6])}  /  Huachitos Ganados: {len(estado_cuenta[7])}\n\nConfiguracion robos: �{estado_cuenta[9]} (energia disponible: {estado_cuenta[10]})  /  �{estado_cuenta[11]}  /  ⚔️{estado_cuenta[12]}\n\nFecha | Nota | Cantidad | Destino / Origen\n:--|:--:|--:|:--:\n",

}
