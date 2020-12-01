import time
import sqlite3

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

    def Enviar_Bineros(self,usuario,cantidad):
        """Registrar transacciones de bineros"""
        
        query = """INSERT INTO transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

        timestamp = time.time()

        try: 
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

        query = """SELECT id,timestamp,cantidad,nota,origen_destino FROM transacciones WHERE usuario=?"""

        query2 = """SELECT id,timestamp,cantidad,origen_destino FROM transacciones WHERE usuario=? AND nota=?"""

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
        
        except Exception as e:
            print(f'----\n{e}')
