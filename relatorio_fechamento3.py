import os
import sys

import mysql.connector
from fpdf import FPDF
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QDateEdit,
    QFileDialog,
    QLabel,
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

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addDays(-7))

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())

        self.generate_button = QPushButton("Gerar Relatório")
        self.generate_button.clicked.connect(self.generate_report)

        layout.addWidget(QLabel("Data Inicial:"))
        layout.addWidget(self.start_date_edit)
        layout.addWidget(QLabel("Data Final:"))
        layout.addWidget(self.end_date_edit)
        layout.addWidget(self.generate_button)

        self.central_widget.setLayout(layout)

    def generate_report(self):
        start_date = self.start_date_edit.date().toString(Qt.ISODate)
        end_date = self.end_date_edit.date().toString(Qt.ISODate)

        query = f"""
            SELECT idlivro, dataAtual, valor, valorfechamento, total, status
            FROM livro
            WHERE dataAtual BETWEEN '{start_date}' AND '{end_date}' AND status = 'F' 
            ORDER BY dataAtual DESC
        """

        cursor = conexao.banco.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        pdf_filename = f"Relatorio_{start_date}_{end_date}.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = []

        header = [
            "ID",
            "Data",
            "Valor Abertura",
            "Valor Fechamento",
            "Total Fechamento",
            "Status",
        ]
        results.insert(0, header)

        table = Table(results)
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

        # Salvar em diretório com data do dia
        save_dir = QFileDialog.getExistingDirectory(self, "Salvar PDFs em", "")
        if save_dir:
            save_path = os.path.join(save_dir, pdf_filename)
            os.rename(pdf_filename, save_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportGenerator()
    window.show()
    sys.exit(app.exec_())
