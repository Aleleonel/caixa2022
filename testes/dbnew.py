# import mysql.connector

from datetime import date

import conexao

dataconsulta = '2022-10-8'
cursor = conexao.banco.cursor()
# sql = """ SELECT
#                 ultupdate
#             FROM
#                 controle_clientes.pedidocaixa
#             LEFT JOIN produtos as p ON cod_produto = p.codigo
#         """
# where = """where pdc.ultupdate = '{}'""".format(dataconsulta)

sql2 = """ SELECT 
                nr_caixa,
                cod_produto,
                p.descricao,
                quantidade,
                valor_total,
                ultupdate

            FROM 
                controle_clientes.pedidocaixa as pdc
            LEFT JOIN produtos as p ON cod_produto = p.codigo
        """

where = """where pdc.ultupdate = '{}'""".format(dataconsulta)
# where = ""
# if str(self.data_value):
#     # data = (self.data_value.strftime('%d-%m-%Y'))
#     where = """ where ultupdate >= """ + str(self.data_value)

comando_sql = sql2+where

cursor.execute(comando_sql)
result = cursor.fetchall()

x = [x for x in result]
print(x)
