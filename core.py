import time
import sqlite3
import operator

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

        query = """SELECT * FROM transacciones WHERE usuario=?"""

        try:
            self.cursor.execute(query,(usuario,))

            resultado = self.cursor.fetchall()

            if resultado != []:
                for item in resultado:
                    if usuario in item:
                        return True
                         
            else:
                return False
        
        except Exception as e:
            print(f'----\n{e}')  

    def Enviar_Bineros(self,usuario,cantidad,asalto=False,pension=False):
        """Registrar transacciones de bineros"""
        
        query = """INSERT INTO transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

        timestamp = time.time()

        try: 
            #Ajuste en caso de comando !asalto
            if asalto == True:
                self.cursor.execute(query,(timestamp,usuario,5,"Asalto",self.id))

                self.cursor.execute(query,(timestamp,self.id,-5,"Asalto",usuario))

                self.conn.commit()

            #Ajuste en caso de entregar pension
            elif pension == True:

                if cantidad == 50:

                    categoria = "Pension Mujicana Basica"

                elif cantidad == 60:

                    categoria = "Pension Mujicana Intermedia"

                elif cantidad == 70:

                    categoria = "Pension Mujicana Avanzada"

                self.cursor.execute(query,(timestamp,usuario,cantidad,categoria,self.id))

                negativo =  cantidad - (cantidad * 2)

                self.cursor.execute(query,(timestamp,self.id,negativo,categoria,usuario))

                self.conn.commit()

            else:
                self.cursor.execute(query,(timestamp,usuario,cantidad,"Deposito",self.id))

                negativo =  cantidad - (cantidad * 2)

                self.cursor.execute(query,(timestamp,self.id,negativo,"Retiro",usuario))

                self.conn.commit()

        except Exception as e:
            print(f'----\n{e}')

    def Consultar_Saldo(self):
        """Consulta el saldo total del cliente"""

        query = """SELECT SUM(cantidad) FROM transacciones WHERE usuario=?"""

        try:
            self.cursor.execute(query,(self.id,))

            resultado = self.cursor.fetchall()

            return resultado[0][0]
        
        except Exception as e:
            print(f'----\n{e}')  
    
    def Historial_Cuenta(self,tipo_movimiento):
        """Consultar historial de movimientos del cliente desde el inicio de la cuenta"""

        query = """SELECT id,timestamp,cantidad,nota,origen_destino FROM transacciones WHERE usuario=? ORDER BY id DESC"""

        query2 = """SELECT id,timestamp,cantidad,origen_destino FROM transacciones WHERE usuario=? AND nota=? ORDER BY id DESC"""

        try:

            if tipo_movimiento == "Global":

                self.cursor.execute(query,(self.id,))

                resultado = self.cursor.fetchall()

                return resultado

            elif tipo_movimiento == "Retiro":

                self.cursor.execute(query2,(self.id,tipo_movimiento))

                resultado = self.cursor.fetchall()

                return resultado

            elif tipo_movimiento == "Deposito":

                self.cursor.execute(query2,(self.id,tipo_movimiento))

                resultado = self.cursor.fetchall()

                return resultado

            elif tipo_movimiento == "Asalto":

                self.cursor.execute(query2,(self.id,tipo_movimiento))

                resultado = self.cursor.fetchall()

                return resultado
        
        except Exception as e:
            print(f'----\n{e}')
    
    def Ranking(self):
        """Forbes Mujico - Usuarios Abinerados"""

        #Obtener lista de usuarios
        clientes = list()
        
        query = """SELECT usuario FROM transacciones WHERE nota='Bono Inicial'"""

        for item in self.cursor.execute(query).fetchall():
            clientes.append(item[0])

        #Obtener balance por usuario y anexar resultados a un diccionario
        rank = {}

        query2 = """SELECT SUM(cantidad) FROM transacciones WHERE usuario = ?"""

        for cliente in clientes:
        
            cantidad = self.cursor.execute(query2,(cliente,)).fetchall()

            rank[cliente] = cantidad[0][0]

        return sorted(rank.items(), key=operator.itemgetter(1), reverse=True)