import mysql.connector
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

import conexao


class SearchProdutos(QDialog):
    def __init__(self, parent=None):
        super(SearchProdutos, self).__init__(parent)
        self.setWindowTitle("CONSULTA DE PRODUTOS")

        self.createUI()

    def createUI(self):
        self.groupBoxCadastro = self.createCadastroGroupBox()
        self.groupBoxConsulta = self.createConsultaGroupBox()
        self.groupBoxSair = self.createSairGroupBox()

        self.disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        self.disableWidgetsCheckBox.toggled.connect(self.toggleGroupBox)

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)
        topLayout.addWidget(self.disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.groupBoxCadastro, 1, 0, 1, 2)
        mainLayout.addWidget(self.groupBoxConsulta, 2, 0, 1, 2)
        mainLayout.addWidget(self.groupBoxSair, 4, 1, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    def createCadastroGroupBox(self):
        groupBoxCadastro = QGroupBox("Cadastro de Itens")
        layout = QFormLayout()

        self.uninput = QLineEdit()
        self.uninput.setFixedSize(35, 25)

        self.cdprod = QLineEdit()
        self.cdprod.returnPressed.connect(self.consultaCodigolist)
        self.cdprod.setFixedSize(60, 25)

        self.eanprod = QLineEdit()
        self.eanprod.setFixedSize(100, 25)

        self.gtinprod = QLineEdit()
        self.gtinprod.setFixedSize(200, 25)

        layout.addRow("Unidade de Medida:", self.uninput)
        layout.addRow("Código:", self.cdprod)
        layout.addRow("EAN:", self.eanprod)
        layout.addRow("GTIN:", self.gtinprod)

        groupBoxCadastro.setLayout(layout)
        return groupBoxCadastro

    def createConsultaGroupBox(self):
        groupBoxConsulta = QGroupBox("Consulta de Produtos")
        layout = QVBoxLayout()

        self.combo = QComboBox()
        self.combo.currentTextChanged.connect(self.consultaProdutolist)
        self.combo.setFixedSize(447, 25)

        self.label_custo = QLabel("Preço de Custo")
        self.precocusto = QLineEdit()
        self.precocusto.setFixedSize(107, 25)

        self.label_venda = QLabel("Preço de Venda")
        self.preco = QLineEdit()
        self.preco.setFixedSize(107, 25)

        layout.addWidget(self.combo)
        layout.addWidget(self.label_custo)
        layout.addWidget(self.precocusto)
        layout.addWidget(self.label_venda)
        layout.addWidget(self.preco)

        groupBoxConsulta.setLayout(layout)
        return groupBoxConsulta

    def createSairGroupBox(self):
        groupBoxSair = QGroupBox("Sair da Consulta")
        layout = QGridLayout()

        self.limpacampos = QPushButton("Limpar")
        self.limpacampos.setDefault(True)
        self.limpacampos.clicked.connect(self.clearFields)

        self.defaultPushButton2 = QPushButton("Fechar")
        self.defaultPushButton2.setDefault(True)
        self.defaultPushButton2.clicked.connect(self.closeConsulta)

        layout.addWidget(self.limpacampos, 2, 0, 1, 2)
        layout.addWidget(self.defaultPushButton2, 3, 0, 1, 2)
        layout.setRowStretch(5, 1)

        groupBoxSair.setLayout(layout)
        return groupBoxSair

    def consultaProdutolist(self):
        consulta = self.combo.currentText().strip().upper()

        if consulta:
            self.cursor = conexao.banco.cursor()
            self.cursor.execute(
                f"SELECT codigo, descricao, ncm, un, preco, est.preco_compra FROM produtos INNER JOIN estoque AS est ON produtos.codigo = est.idproduto WHERE descricao = '{consulta}'"
            )

            result = self.cursor.fetchone()
            self.acceptcursor.close()

            if result:
                self.display_results(result)
            else:
                self.show_warning_message(
                    "Produto não encontrado ou sem movimentação em estoque!"
                )

    def consultaCodigolist(self):
        consultacodigo = self.cdprod.text()

        if consultacodigo:
            self.cursor = conexao.banco.cursor()
            self.cursor.execute(
                f"SELECT codigo, descricao, ncm, un, preco, est.preco_compra FROM produtos INNER JOIN estoque AS est ON produtos.codigo = est.idproduto WHERE codigo = '{consultacodigo}'"
            )

            result = self.cursor.fetchone()
            self.cursor.close()

            if result:
                self.display_results(result)
            else:
                self.show_warning_message(
                    "Produto não encontrado ou sem movimentação em estoque!"
                )

    def display_results(self, result):
        self.cdprod.setText(str(result[0]))
        self.combo.addItem(result[1])
        self.eanprod.setText(str(result[2]))
        self.uninput.setText(str(result[3]))
        self.preco.setText(str(result[4]))
        self.precocusto.setText(str(result[5]))
        self.gtinprod.setText("")

    def show_warning_message(self, message):
        QMessageBox.warning(self, "Consulta de Produtos", message)

    def closeConsulta(self):
        self.conexao.banco.close()
        self.close()

    def clearFields(self):
        self.combo.clear()
        self.cdprod.clear()
        self.eanprod.clear()
        self.uninput.clear()
        self.preco.clear()
        self.precocusto.clear()
        self.gtinprod.clear()

    def toggleGroupBox(self, checked):
        self.groupBoxCadastro.setDisabled(checked)
        self.groupBoxConsulta.setDisabled(checked)
        self.groupBoxSair.setDisabled(checked)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    searchProdutos = SearchProdutos()
    searchProdutos.show()
    sys.exit(app.exec_())
