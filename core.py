import time
from datetime import datetime
import sqlite3
import operator
import random
import string
import json

class HuachiNet():
    """Huachicol as a service
    ---------------------------------
    Requiere nombre de usuario para obtener la siguiente informacion:
    -Saldo total
    -Historial de movimientos (Global,Depositos,Retiros)

    El usuario puede realizar las siguientes funciones dentro de la red:
    
    -Bono_Bienvenida
    -Verificar_Usuario
    -Enviar_Bineros

    *Si el usuario no existe en la BD, se regresa None como valor
    """

    def __init__(self,usuario):
        #Conexion a BD
        self.conn = sqlite3.connect("boveda.sqlite3")

        self.cursor = self.conn.cursor()

        self.id = usuario

        self.perk, self.power, self.trait, self.weapon, self.guild = self.Consultar_Perks()

        self.stats = self.Calcular_Stats()

        self.saldo_total = self.Consultar_Saldo()

        self.historial = self.Historial_Cuenta()

        self.depositos = self.Historial_Cuenta(tipo_movimiento="Deposito")

        self.retiros = self.Historial_Cuenta(tipo_movimiento="Retiro")

        self.asaltos = self.Historial_Cuenta(tipo_movimiento="Asalto")

        self.huachitos = self.Historial_Cuenta(tipo_movimiento="Huachito")

        self.premios_huachito = self.Historial_Cuenta(tipo_movimiento="Premio Huachito")

        self.atracos = self.Historial_Cuenta(tipo_movimiento="Atraco")

        self.levantones = self.Historial_Cuenta(tipo_movimiento="Levanton")


    def Verificar_Usuario(self,usuario):
        """Verificar si existe el cliente en la BD"""

        existe = False

        query = """SELECT ID FROM transacciones WHERE usuario=? LIMIT 1"""

        resultado = self.cursor.execute(query,(usuario,)).fetchone()

        if resultado != None:

            existe = True

        return existe

    def Bono_Bienvenida(self,usuario):
        """Entregar bineros a los clientes nuevos"""

        if self.Verificar_Usuario(usuario) == False:

            query = """INSERT INTO transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

            timestamp = time.time()
        
            self.cursor.execute(query,(timestamp,usuario,1000,"Bono Inicial","Bodega"))

            self.cursor.execute(query,(timestamp,"Bodega",-1000,"Retiro",usuario))

            self.conn.commit()

    def Enviar_Bineros(self,usuario,cantidad,nota="Default"):
        """Registrar transacciones de bineros"""
        
        query = """INSERT INTO transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

        timestamp = time.time()

        self.Bono_Bienvenida(usuario)
        
        if nota == "Default":

            self.cursor.execute(query,(timestamp,usuario,cantidad,"Deposito",self.id))

            negativo =  cantidad - (cantidad * 2)

            self.cursor.execute(query,(timestamp,self.id,negativo,"Retiro",usuario))

            self.conn.commit()

        elif nota != "Default":

            self.cursor.execute(query,(timestamp,usuario,cantidad,nota,self.id))

            negativo =  cantidad - (cantidad * 2)

            self.cursor.execute(query,(timestamp,self.id,negativo,nota,usuario))

            self.conn.commit()


    def Consultar_Saldo(self):
        """Consulta el saldo total del cliente"""

        query = """SELECT SUM(cantidad) FROM transacciones WHERE usuario=?"""

        self.cursor.execute(query,(self.id,))

        resultado = self.cursor.fetchone()

        return resultado[0]
        

    def Historial_Cuenta(self, tipo_movimiento = "Global"):
        """Consultar historial de movimientos del cliente desde el inicio de la cuenta"""
        
        if tipo_movimiento == "Global":

            query = """SELECT id,timestamp,cantidad,nota,origen_destino FROM transacciones WHERE usuario=? ORDER BY id DESC"""
            
            parametros = (self.id,)

        else:
                
            query = """SELECT id,timestamp,cantidad,origen_destino FROM transacciones WHERE usuario=? AND nota=? ORDER BY id DESC"""
                
            parametros = (self.id,tipo_movimiento)

        return self.cursor.execute(query,parametros).fetchall()
        
             
    def Mujicanos(self):
        """Lista de usuarios activos"""

        #Obtener lista de usuarios
        query = """SELECT usuario FROM transacciones WHERE nota='Bono Inicial'"""

        self.cursor.row_factory = lambda cursor, row: row[0]

        resultado = self.cursor.execute(query).fetchall()

        return list(filter(None,resultado))

    def Ranking(self):
        """Forbes Mujico - Usuarios Abinerados"""

        #Obtener lista de usuarios
        query = """SELECT usuario, SUM(cantidad) as cantidad FROM transacciones WHERE usuario in (SELECT usuario FROM transacciones WHERE nota='Bono Inicial') GROUP BY usuario ORDER BY cantidad DESC"""
        
        return self.cursor.execute(query).fetchall()

    def Huachiclave(self):
        """Regresa la huachiclave vigente o genera una nueva"""

        query = """SELECT timestamp,huachiclave,cantidad,entregado FROM huachilate WHERE entregado = '0' ORDER BY timestamp"""

        query2 = """INSERT INTO huachilate (timestamp,huachiclave,cantidad,entregado) VALUES (?,?,?,?)"""

        resultado = self.cursor.execute(query).fetchall()

        if resultado == []:
            
            timestamp = time.time()
            
            huachiclave = "".join(random.choices(string.ascii_letters + string.digits,k = 7))

            cantidad = random.randint(5000,50000)

            self.cursor.execute(query2,(timestamp,huachiclave,cantidad,0))

            self.conn.commit()

            return (timestamp,huachiclave,cantidad)
        
        else:
            return resultado[-1]

    def Consultar_Perks(self):
        """Consultar perk, power, trait , arma y guild"""

        query = """SELECT perk,power,trait,weapon,guild FROM perks WHERE usuario = ?"""

        resultado = self.cursor.execute(query,(self.id,)).fetchall()

        #En caso de que el usuario no este en la tabla de perks, se añadira con stats basicos.
        if resultado == []:

            timestamp = time.time()
            
            query2 = """INSERT INTO perks (timestamp,usuario,perk,power,trait,weapon,guild) VALUES (?,?,?,?,?,?,?)"""

            self.cursor.execute(query2,(timestamp,self.id,"Normal",100,"Normal","Navaja","Normal"))

            self.conn.commit()

            return ("Normal",100,"Normal","Navaja","Normal")

        else:

            return resultado[-1]

    def Update_Perks(self,clase,item):
        """Agregar y modificar perk,trait, weapon y guild de los mujicanos"""

        query = f"""UPDATE perks SET {clase} = ? WHERE usuario = ?"""

        query2 = """UPDATE perks SET power = 100 WHERE usuario = ?"""

        self.cursor.execute(query,(item,self.id))

        if clase == "perk":

            self.cursor.execute(query2,(self.id,))

        self.conn.commit()

    def Consumir_Energia(self,cantidad):
        """Los perks necesitan energia para funcionar"""

        energia = self.power - cantidad

        query = """UPDATE perks SET power = ? WHERE usuario = ?"""

        self.cursor.execute(query,(energia,self.id))

        self.conn.commit()

    def Enviar_Shares(self,usuario,cantidad,share,precio):
        """Huachiswap"""

        query = """INSERT INTO shares (timestamp,usuario,cantidad,share,precio,origen_destino) VALUES (?,?,?,?,?,?)"""

        timestamp = time.time()

        self.cursor.execute(query,(timestamp,usuario,cantidad,share,precio,self.id)) 

        negativo = cantidad - (cantidad * 2)

        self.cursor.execute(query,(timestamp,self.id,negativo,share,precio,usuario))

        self.conn.commit()

    def Consultar_Shares(self):
        """Consulta tu portafolio"""

        query = """ SELECT share, SUM(cantidad) as cantidad, AVG(precio) as precio FROM shares WHERE usuario = ? AND share in (SELECT share FROM shares WHERE usuario = ?) GROUP BY share ORDER BY cantidad DESC"""

        return self.cursor.execute(query,(self.id,self.id)).fetchall()

    def Calcular_Stats(self):
        """NRPG - Niño Rata Playing Game"""

        baseStats = {"ConductoresNocturnos" : [70,50,40,40],
                     "AlianzaOtako" : [30,70,40,60],
                     "DominioNalgoticas" : [70,30,60,40],
                     "Corvidos" : [40,60,40,60],
                     "Normal" : [50,50,50,50]}

        perkStats = json.loads(open("./assets/perks.json","r",encoding="utf-8").read())

        traitStats = json.loads(open("./assets/traits.json","r",encoding="utf-8").read())

        weaponStats = json.loads(open("./assets/weapons.json","r",encoding="utf-8").read())

        #Stats base + perks stats
        base = baseStats[self.guild]

        perk = perkStats[self.perk]

        trait = traitStats[self.trait]

        weapon = weaponStats[self.weapon]

        return [ base[i] + perk[i] + trait[i] + weapon[i] for i in range(4) ]
    
   
