import sys
from datetime import datetime

import mysql.connector
from PyQt5.QtWidgets import (
    QApplication,
    QDateEdit,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

import conexao


class DateRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selecionar Range de Data")
        self.layout = QVBoxLayout()

        self.label_start = QLabel("Data Inicial:")
        self.date_start = QDateEdit()
        self.date_start.setDate(datetime.today().date())

        self.label_end = QLabel("Data Final:")
        self.date_end = QDateEdit()
        self.date_end.setDate(datetime.today().date())

        self.btn_generate = QPushButton("Visualizar Dados")
        self.btn_generate.clicked.connect(self.show_report_data)

        self.layout.addWidget(self.label_start)
        self.layout.addWidget(self.date_start)
        self.layout.addWidget(self.label_end)
        self.layout.addWidget(self.date_end)
        self.layout.addWidget(self.btn_generate)

        self.setLayout(self.layout)

    def show_report_data(self):
        start_date = self.date_start.date().toPyDate()
        end_date = self.date_end.date().toPyDate()

        query = "SELECT idlivro, dataAtual, valor, valorfechamento, total FROM livro WHERE status = 'F' AND dataAtual BETWEEN %s AND %s"
        cursor = conexao.banco.cursor()
        cursor.execute(query, (start_date, end_date))
        data = cursor.fetchall()

        cursor.close()

        data_dialog = QDialog(self)
        data_dialog.setWindowTitle("Dados do Relatório")
        data_layout = QVBoxLayout()

        table_widget = QTableWidget()
        table_widget.setColumnCount(5)
        table_widget.setHorizontalHeaderLabels(
            ["ID", "Data", "Valor Abertura", "Valor Fechamento", "Total Fechamento"]
        )

        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                table_widget.setItem(row_index, col_index, item)

        data_layout.addWidget(table_widget)
        data_dialog.setLayout(data_layout)
        data_dialog.exec_()


class ReportGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Relatório de Fechamento de Caixa")
        self.setGeometry(100, 100, 400, 200)

        self.btn_generate = QPushButton("Gerar Relatório", self)
        self.btn_generate.clicked.connect(self.show_date_range_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_generate)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_date_range_dialog(self):
        date_range_dialog = DateRangeDialog(self)
        date_range_dialog.exec_()

    # Resto do código permanece igual...
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
