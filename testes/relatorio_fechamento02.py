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

import conexao


# Classe para a janela principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Relatório de Fechamento de Caixa")
        self.setGeometry(100, 100, 400, 300)

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
        """

        cursor = conexao.banco.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(
            200,
            10,
            f"Relatório de Fechamento de Caixa de {start_date} a {end_date}",
            ln=True,
            align="C",
        )

        for row in results:
            pdf.cell(40, 10, f"ID Livro: {row['idlivro']}", ln=True)
            pdf.cell(40, 10, f"Data: {row['dataAtual']}", ln=True)
            pdf.cell(40, 10, f"Valor Abertura: R${row['valor']:.2f}", ln=True)
            pdf.cell(
                40, 10, f"Valor Fechamento: R${row['valorfechamento']:.2f}", ln=True
            )
            pdf.cell(
                40,
                10,
                f"Total do Fechamento: R${row['total']:.2f}",
                ln=True,
            )
            pdf.cell(40, 10, f"Status: {row['status']}", ln=True)
            pdf.ln()

        save_dir = QFileDialog.getExistingDirectory(self, "Salvar PDFs em", "")
        if save_dir:
            filename = f"Relatorio_{start_date}_{end_date}.pdf"
            save_path = f"{save_dir}/{filename}"
            pdf.output(save_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
