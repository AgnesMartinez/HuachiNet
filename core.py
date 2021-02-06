import time
import sqlite3
import operator
import random
import string

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
        self.saldo_total = self.Consultar_Saldo()
        self.historial = self.Historial_Cuenta("Global")
        self.depositos = self.Historial_Cuenta("Deposito")
        self.retiros = self.Historial_Cuenta("Retiro")
        self.asaltos = self.Historial_Cuenta("Asalto")
        self.huachitos = self.Historial_Cuenta("Huachito")
        self.premios_huachito = self.Historial_Cuenta("Premio Huachito")
        self.atracos = self.Historial_Cuenta("Atraco")
        self.levantones = self.Historial_Cuenta("Levanton")


    def Bono_Bienvenida(self,usuario):
        """Entregar bineros a los clientes nuevos"""

        query = """INSERT INTO transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

        timestamp = time.time()

        try: 
            self.cursor.execute(query,(timestamp,usuario,1000,"Bono Inicial","Bodega"))

            self.cursor.execute(query,(timestamp,"Bodega",-1000,"Retiro",usuario))

            self.conn.commit()

        except Exception as e:
            print(f'----\n{e}')
    
    def Verificar_Usuario(self,usuario):
        """Verificar si existe el cliente en la BD"""

        existe = False

        query = """SELECT ID FROM transacciones WHERE usuario=? LIMIT 1"""

        try:
            self.cursor.execute(query,(usuario,))

            resultado = self.cursor.fetchone()

            print(resultado)

            if resultado != None:
                existe = True

        except Exception as e:
            print(f'----\n{e}')

        return existe

    def Enviar_Bineros(self,usuario,cantidad,nota="Default"):
        """Registrar transacciones de bineros"""
        
        query = """INSERT INTO transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

        timestamp = time.time()

        try:
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

        except Exception as e:
            print(f'----\n{e}')

    def Consultar_Saldo(self):
        """Consulta el saldo total del cliente"""

        query = """SELECT SUM(cantidad) FROM transacciones WHERE usuario=?"""

        try:
            self.cursor.execute(query,(self.id,))

            resultado = self.cursor.fetchone()

            return resultado[0][0]
        
        except Exception as e:
            print(f'----\n{e}')  
    
    def Historial_Cuenta(self, tipo_movimiento = "Global"):
        """Consultar historial de movimientos del cliente desde el inicio de la cuenta"""
        try:
            if tipo_movimiento == "Global":
                query = """SELECT id,timestamp,cantidad,nota,origen_destino FROM transacciones WHERE usuario=? ORDER BY id DESC"""
                parametros = (self.id,)

            else:
                query2 = """SELECT id,timestamp,cantidad,origen_destino FROM transacciones WHERE usuario=? AND nota=? ORDER BY id DESC"""
                parametros = (self.id,tipo_movimiento)

            self.cursor.execute(query,parametros)

            resultado = self.cursor.fetchall()

            return resultado
        
        except Exception as e:
            print(f'----\n{e}')
    
    def Mujicanos(self):
        """Lista de usuarios activos"""

        #Obtener lista de usuarios
        query = """SELECT usuario FROM transacciones WHERE nota='Bono Inicial'"""

        self.cursor.row_factory = lambda cursor, row: row[0]

        resultado = self.cursor.execute(query).fetchall()

        return list(filter(None,resultado))

    def Ranking(self, limite = '25'):
        """Forbes Mujico - Usuarios Abinerados"""

        #Obtener lista de usuarios
        query = """SELECT usuario, SUM(cantidad) as cantidad FROM transacciones WHERE usuario in (SELECT usuario FROM transacciones WHERE nota='Bono Inicial') GROUP BY usuario ORDER BY cantidad DESC LIMIT ? """
        

        return self.cursor.execute(query,(limite,)).fetchall()

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
