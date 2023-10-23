import os
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle

# def printer(self):
#     self.cursor = conexao.banco.cursor()
#     comando_sql = """
#                     select
#                         p.codigo,
#                         p.descricao,
#                         e.quantidade,
#                         p.preco,
#                         e.valor_total
#                     from
#                         produtos p
#                     inner join pedidocaixa e on p.codigo = e.cod_produto
#                     AND nr_caixa = {0}""".format(
#         str(self.nr_caixa)
#     )

#     self.cursor.execute(comando_sql)
#     dados_lidos = self.cursor.fetchall()
#     y = 0
#     pdf = canvas.Canvas("recibo.pdf")
#     pdf.setFont("Times-Bold", 18)
#     pdf.drawString(90, 800, "MINA & MINEKO ART. FAMELE:")
#     pdf.setFont("Times-Bold", 12)

#     pdf.drawString(10, 750, "COD")
#     pdf.drawString(50, 750, "PRODUTO")
#     pdf.drawString(260, 750, "QTD.")
#     pdf.drawString(310, 750, "PREÇO UN.")
#     pdf.drawString(390, 750, "SUB.TOTAL")
#     pdf.drawString(470, 750, "TOTAL")
#     pdf.drawString(
#         3,
#         750,
#         "________________________________________________________________________________________",
#     )

#     total = 0
#     subtotal = 0
#     for i in range(0, len(dados_lidos)):
#         y += 50
#         # CODIGO PRODUTO
#         pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
#         # DESCRIÇAO PRODUTO
#         pdf.drawString(50, 750 - y, str(dados_lidos[i][1]))
#         # QUANTIDADE VENDIDA
#         pdf.drawString(260, 750 - y, str(dados_lidos[i][2]))
#         # PREÇO UNITARIO
#         pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
#         subtotal = (dados_lidos[i][3]) * dados_lidos[i][2]  # QTD x PREÇO UNITARIO
#         total += subtotal
#         pdf.drawString(390, 750 - y, str(subtotal))  # SUB TOTAL
#     pdf.drawString(470, 750 - y, str(total))  # TOTAL

#     pdf.save()
# dlg = telaprincipal()
# dlg.exec()

# def printer(self):
#     # Data atual
#     current_date = datetime.now().strftime("%Y-%m-%d")

#     # Consulta ao banco de dados
#     self.cursor = conexao.banco.cursor()
#     comando_sql = """
#         select
#             p.codigo,
#             p.descricao,
#             e.quantidade,
#             p.preco,
#             e.valor_total
#         from
#             produtos p
#         inner join pedidocaixa e on p.codigo = e.cod_produto
#         AND nr_caixa = {0}""".format(
#         str(self.nr_caixa)
#     )

#     self.cursor.execute(comando_sql)
#     dados_lidos = self.cursor.fetchall()

#     # Nome do arquivo com a data atual e número do caixa
#     pdf_filename = f"Recibo_Caixa{self.nr_caixa}_{current_date}.pdf"

#     doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
#     story = []

#     header = [
#         "COD",
#         "PRODUTO",
#         "QTD.",
#         "PREÇO",
#         "SUB.",
#         "TOTAL",
#     ]

#     results = [header]

#     for row in dados_lidos:
#         results.append(list(map(str, row)))  # Incluindo a coluna 'valor_total'

#     table = Table(results)
#     table.setStyle(
#         TableStyle(
#             [
#                 ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
#                 ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
#                 ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#                 ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#                 ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
#                 ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
#                 ("GRID", (0, 0), (-1, -1), 1, colors.black),
#             ]
#         )
#     )

#     # Adicione mais elementos à história, se necessário
#     story.append(table)
#     story.append(Spacer(1, 12))

#     # Salvar o arquivo automaticamente
#     doc.build(story)

#     dlg = telaprincipal()
#     dlg.exec()

#     return pdf_filename

# def printer(self):
#     # Data atual
#     current_date = datetime.now().strftime("%Y-%m-%d")

#     # Consulta ao banco de dados
#     self.cursor = conexao.banco.cursor()
#     comando_sql = """
#         select
#             p.codigo,
#             p.descricao,
#             e.quantidade,
#             p.preco,
#             e.valor_total
#         from
#             produtos p
#         inner join pedidocaixa e on p.codigo = e.cod_produto
#         AND nr_caixa = {0}""".format(
#         str(self.nr_caixa)
#     )

#     self.cursor.execute(comando_sql)
#     dados_lidos = self.cursor.fetchall()

#     # Somatório do total do pedido
#     total_pedido = sum(row[4] for row in dados_lidos)

#     # Nome do arquivo com a data atual e número do caixa
#     pdf_filename = f"Recibo_Caixa{self.nr_caixa}_{current_date}.pdf"

#     doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
#     story = []

#     styles = getSampleStyleSheet()
#     styleN = styles["Normal"]
#     styleH = styles["Heading1"]

#     # Cabeçalho
#     story.append(Paragraph("Recibo", styleH))
#     story.append(Spacer(1, 12))

#     header = [
#         "COD",
#         "PRODUTO",
#         "QTD.",
#         "PREÇO",
#         "SUBTOTAL",
#     ]

#     results = [header]

#     for row in dados_lidos:
#         subtotal = row[3] * row[2]  # Preço x Quantidade
#         results.append(
#             [str(row[0]), row[1], str(row[2]), str(row[3]), str(subtotal)]
#         )

#     table = Table(results)
#     table.setStyle(
#         TableStyle(
#             [
#                 ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
#                 ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
#                 ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#                 ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#                 ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
#                 ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
#                 ("GRID", (0, 0), (-1, -1), 1, colors.black),
#             ]
#         )
#     )

#     # Adicione a tabela à história
#     story.append(table)
#     story.append(Spacer(1, 12))

#     # Total do pedido
#     story.append(Paragraph(f"Total do Pedido: R${total_pedido:.2f}", styleN))

#     # Salvar o arquivo automaticamente
#     doc.build(story)

#     dlg = telaprincipal()
#     dlg.exec()

#     return pdf_filename
