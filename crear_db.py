import sqlite3
import time
from datetime import datetime

#Conexion a BD
conn = sqlite3.connect('boveda.sqlite3')
tabla_t = """CREATE TABLE IF NOT EXISTS transacciones (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp VARCHAR(255),
    usuario VARCHAR(255),
    cantidad INTEGER,
    nota VARCHAR(255),
    origen_destino VARCHAR(255))"""

tabla_comentario = """CREATE TABLE IF NOT EXISTS comentarios (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    id_comment VARCHAR(255) UNIQUE)"""

tabla_rifa = """CREATE TABLE IF NOT EXISTS huachilate (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp VARCHAR(255),
    huachiclave VARCHAR(255),
    cantidad INTEGER,
    entregado INTEGER)"""

tabla_boletitos = """CREATE TABLE IF NOT EXISTS boletitos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp VARCHAR(255),
    usuario VARCHAR(255),
    huachiclave VARCHAR(255)
)"""

index4 = """CREATE INDEX IF NOT EXISTS ind_usuario ON boletitos (usuario)"""

index3 = """CREATE INDEX IF NOT EXISTS ind_huachiclave ON huachilate (huachiclave)"""

index2 = """CREATE INDEX IF NOT EXISTS ind_comentario ON comentarios (id_comment)"""

index = """CREATE INDEX IF NOT EXISTS ind_usuario ON transacciones (usuario)"""

genesis = """INSERT into transacciones (timestamp,usuario,cantidad,nota,origen_destino) VALUES (?,?,?,?,?)"""

cursor =  conn.cursor()

cursor.execute(tabla_t)

cursor.execute(index)

cursor.execute(genesis,(time.time(),"Bodega",10000000,"Deposito","Genesis"))

cursor.execute(tabla_comentario)

cursor.execute(index2)

cursor.execute(tabla_rifa)

cursor.execute(index3)

cursor.execute(tabla_boletitos)

cursor.execute(index4)

conn.commit()



