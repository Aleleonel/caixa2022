import sys

import mysql.connector
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

import conexao


class ReportGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Relatório de Fechamento de Caixa")
        self.setGeometry(100, 100, 400, 200)

        self.btn_generate = QPushButton("Gerar Relatório", self)
        self.btn_generate.clicked.connect(self.generate_report)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_generate)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_report(self):
        # Consulta ao banco de dados
        query = "SELECT idlivro, dataAtual, valor, valorfechamento, total FROM livro WHERE status = 'F'"
        cursor = conexao.banco.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # Desconectar do banco de dados
        cursor.close()
        # banco.close()

        # Criar o PDF
        pdf_filename, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF", "", "PDF Files (*.pdf)"
        )

        if pdf_filename:
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            story = []

            # Cabeçalho
            header = [
                "ID",
                "Data",
                "Valor Abertura",
                "Valor Fechamento",
                "Total Fechamento",
            ]
            data.insert(0, header)

            # Criar a tabela
            table = Table(data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            story.append(table)
            doc.build(story)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportGenerator()
    window.show()
    sys.exit(app.exec_())
