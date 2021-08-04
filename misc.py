
shops = {
  'stonks' : ("AAPL","AMZN","TSLA","MRNA","NFLX","NVDA","NIO","WMT","COST","TUP","GME","NTDOY","SNE","MSFT","INTC","AMD","BTC-USD","ETH-USD","LTC-USD","VET-USD","NANO-USD","DOGE-USD"),

  'opciones shop' : ("monachina","trapo","furro","nalgotica","cura","corvido","galleta","huachito","chambeadora","valentin"),
  
  'menu shop' : ("Menu Shop","__HuachiStore - Abierto cuando llegamos, cerrado cuando nos vamos__\n\nEnvia un regalo usando el comando shop, seguido de una opcion del menu, todo a 5 huachis.\n\nRegalo | subcomando\n:--|--:\nMonas Chinas | monachina\nTrapitos | trapo\nFurros | furro\nHuachito | huachito\nNalgoticas | nalgotica\nMDLP | cura / corvido\nGanosas (Revistas para adultos) | chambeadora\nGalleta de la fortuna | galleta\n\nCompleta tu compra de la siguiente manera:\n\n    shop comando\n\n    Ejemplo: shop monachina\n\n    (no olvides el signo de exclamación)\n\nUsalo en la seccion de comentarios."),

  #Menus por guilds
  'AlianzaOtako' : ("Huachibonos - Alianza Otako","__Huachibonos - Kawaii desu ne! Tenemos los mejores precios de la region__\n\nRecuerda que los huachibonos 🌀 consumen energia! Para recargar tu huachibono 🌀 necesitas comprar uno nuevo. La energia no es acumulable.\n\nCosto por huachibono: 🌀 = 800  🎭 = 400  ⚔️ = 200\n\nHuachibono | subcomando\n:--|--:\nGenkidama 🌀 | genkidama\nImpactTrueno 🌀 | pikachu\nPolvoDiamante 🌀 | diamante\nRasegan 🌀 | naruto\nOmaewamushinderu 🌀 | omaewa\nEsferaDragon 🎭 | dragonball\nPuerta Magica 🎭 | doraemon\nPiedraEvolutiva 🎭 | piedra\nSemilla Hermitaño 🎭 | semilla\nTesticulos Exodia 🎭 | exodia\nDakimakura ⚔️ | waifu\nMegaBuster ⚔️ | megaman\nCaparazol Azul ⚔️ | caparazon\nSakabato ⚔️ | sakabato\nShinigami ⚔️ | demonio\n\nCompleta tu compra de la siguiente manera:\n\n!huachibono waifu (comando <opcion>)\n\nUsa el comando en la seccion de comentarios."),
  
  'DominioNalgoticas' : ("Huachibonos - Dominio Nalgoticas","__Huachibonos - Bienvenido al gremio mas oscuro y redondo__\n\nRecuerda que los huachibonos 🌀 consumen energia! Para recargar tu huachibono 🌀 necesitas comprar uno nuevo. La energia no es acumulable.\n\nCosto por huachibono: 🌀 = 800  🎭 = 400  ⚔️ = 200\n\nHuachibono | subcomando\n:--|--:\nEl Llamado de Tuculo 🌀 | tuculo\nVision Nalgotica 🌀 | nalgavision\nConxuro 🌀 | conxuro\nLectura de Tarot 🌀 | tarot\nAgua de Calzon Embotellada 🌀 | calzon\nGagBall 🎭 | gagball\nDarketiza 🎭 | tachas\nEdgar Allan Hoe 🎭 | allanhoe\nMuñeco Voodoo 🎭 | budu\nEl Beso de Draculona 🎭 | draculona\nCuenta OnlyFans ⚔️ | onlyfans\nBotas con picos ⚔️ | botas\nLa maldicion del dolor infinito ⚔️ | blueballs\nGothicc ⚔️ | gothic\nTabla Ouija ⚔️ | ouija\n\nCompleta tu compra de la siguiente manera:\n\n!huachibono draculona (comando <opcion>)\n\nUsa el comando en la seccion de comentarios."),
  #huachibonos
  'bonos perks' : {"genkidama" : "Genkidama", 
                   "pikachu" : "ImpactTrueno", 
                   "diamante" : "PolvoDiamante", 
                   "naruto" : "Rasegan", 
                   "omaewa" : "Omaewamushinderu" , 
                   "tuculo" : "LlamadoTuculo", 
                   "nalgavision" : "VisionNalgotica",
                   "conxuro":"Conxuro",
                   "tarot":"LecturaTarot", 
                   "calzon": "AguaCalzon"},

  'bonos traits' : {"dragonball" : "EsferaDragon", 
                    "doraemon" : "PuertaMagica", 
                    "piedra" : "PiedraEvolutiva", 
                    "semilla" : "SemillaHermitaño",
                    "exodia": "TestoExodia", 
                    "gagball" : "GagBall", 
                    "tachas": "Darketiza", 
                    "allanhoe" : "EAHoe", 
                    "budu" : "Voodoo", 
                    "draculona" : "BesoDraculona"},

  'bonos weapons' : {"waifu" : "Dakimakura", 
                     "megaman" : "MegaBuster", 
                     "caparazon" : "CaparazonAzul", 
                     "sakabato" : "Sakabato", 
                     "demonio" : "Shinigami", 
                     "onlyfans" : "OnlyFans", 
                     "botas" : "BotasPicos", 
                     "blueballs" : "DolorInfinito", 
                     "gothic" : "Gothicc", 
                     "ouija" : "TablaOuija"},
  
  'bonos guilds' : {"otakos" : "AlianzaOtako", 
                    "nalgoticas" : "DominioNalgoticas" },

  'bonos opciones' : ["genkidama","pikachu","diamante",
                      "naruto","omaewa","tuculo",
                      "nalgavision","conxuro","tarot",
                      "calzon","dragonball","doraemon",
                      "piedra","semilla","exodia",
                      "gagball","tachas","allanhoe",
                      "budu","dacrulona","waifu",
                      "megaman","caparazon","sakabato",
                      "demonio","onlyfans","botas",
                      "blueballs","gothic","ouija"]

  

}

resp_saldo = open("./assets/frases/frases_saldo.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_envio = open("./assets/frases/frases_envio.txt", "r", encoding="utf-8").read().splitlines()

resp_empleado_error = open("./assets/frases/frases_error.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_cuenta = open("./assets/frases/frases_cuenta.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_sinbineros = open("./assets/frases/frases_sinbineros.txt", "r", encoding="utf-8").read().splitlines()

resp_tip_empleado = open("./assets/frases/frases_empleado.txt", "r", encoding="utf-8").read().splitlines()

resp_shop = open("./assets/frases/frases_shop.txt", "r", encoding="utf-8").read().splitlines()

resp_tumbar_cholo = open("./assets/frases/frases_tumbar_cholo.txt", "r", encoding="utf-8").read().splitlines()

resp_tumbar_victima = open("./assets/frases/frases_tumbar_victima.txt", "r", encoding="utf-8").read().splitlines()

resp_seguridad = open("./assets/frases/frases_seguridad.txt", "r", encoding="utf-8").read().splitlines()

resp_autorobo = open("./assets/frases/frases_autorobo.txt", "r", encoding="utf-8").read().splitlines()

resp_levanton = open("./assets/frases/frases_levanton.txt", "r", encoding="utf-8").read().splitlines()

resp_huachilate = open("./assets/frases/frases_huachilate.txt", "r", encoding="utf-8").read().splitlines()

resp_huachiswap = open("./assets/frases/frases_huachiswap.txt","r",encoding="utf-8").read().splitlines()

monaschinas = open("./assets/shop/monaschinas.txt", "r", encoding="utf-8").read().splitlines()

trapos = open("./assets/shop/trapos.txt", "r", encoding="utf-8").read().splitlines()

furros = open("./assets/shop/furro.txt", "r", encoding="utf-8").read().splitlines()

nalgoticas = open("./assets/shop/nalgoticas.txt", "r", encoding="utf-8").read().splitlines()

curas = open("./assets/shop/curas.txt", "r", encoding="utf-8").read().splitlines()

chambeadoras = open("./assets/shop/ganosas.txt", "r", encoding="utf-8").read().splitlines()

galletas = open("./assets/shop/galletas.txt", "r", encoding="utf-8").read().splitlines()

valentines = open("./assets/shop/valentin.txt", "r", encoding="utf-8").read().splitlines()

