import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def printer(self):
    # Data atual
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Consulta ao banco de dados
    self.cursor = conexao.banco.cursor()
    comando_sql = """
        select
            p.codigo,
            p.descricao,
            e.quantidade,
            p.preco,
            e.valor_total
        from
            produtos p
        inner join pedidocaixa e on p.codigo = e.cod_produto
        AND nr_caixa = {0}""".format(
        str(self.nr_caixa)
    )

    self.cursor.execute(comando_sql)
    dados_lidos = self.cursor.fetchall()

    # Somatório do total do pedido
    total_pedido = sum(row[4] for row in dados_lidos)

    # Nome do arquivo com a data atual e número do caixa
    pdf_filename = f"Recibo_Caixa{self.nr_caixa}_{current_date}.pdf"

    # Defina o diretório onde deseja salvar o arquivo
    save_dir = "/caminho/do/diretorio/"  # Substitua pelo caminho desejado

    # Combine o caminho do diretório com o nome do arquivo
    full_path = os.path.join(save_dir, pdf_filename)

    doc = SimpleDocTemplate(full_path, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()

    # Resto do seu código

    # Salvar o arquivo automaticamente
    doc.build(story)

    dlg = telaprincipal()
    dlg.exec()

    return full_path
