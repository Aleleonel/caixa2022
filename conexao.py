import mysql.connector

banco = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd="",
    database="controle_clientes"
)