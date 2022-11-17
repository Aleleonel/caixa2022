#!/usr/bin/env python


import sys

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QLineEdit, QProgressBar,
                             QPushButton, QRadioButton, QScrollBar,
                             QSizePolicy, QSlider, QSpinBox, QStyleFactory,
                             QTableWidget, QTabWidget, QTextEdit, QVBoxLayout,
                             QWidget)


class CadastroProdutos(QDialog):
    def __init__(self, parent=None):
        super(CadastroProdutos, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox(
            "&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createGroupBoxSalvar()
        self.createGroupBox()

        styleComboBox.activated[str].connect(self.changeStyle)

        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)

        disableWidgetsCheckBox.toggled.connect(self.GroupBox1.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.GroupBox2.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.GroupBox3.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox1, 1, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox2, 2, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox3, 4, 1, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("CADASTRO DE PRODUTOS")
        self.changeStyle('Windows')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def createTopLeftGroupBox(self):
        self.GroupBox1 = QGroupBox("Cadastro de Itens")

        # Insere o ramo ou tipo /
        self.uninput = QComboBox()
        self.uninput.addItem("UN")
        self.uninput.addItem("PÇ")
        self.uninput.addItem("KG")
        self.uninput.addItem("LT")
        self.uninput.addItem("PT")
        self.uninput.addItem("CX")

        self.codigo_produto = QLabel("Codigo")
        cdprod = QLineEdit()
        self.codigo_produto.setAlignment(Qt.AlignLeft)

        self.codigo_ean = QLabel("EAN")
        eanprod = QLineEdit()
        self.codigo_ean.setAlignment(Qt.AlignCenter)

        self.codigo_gtin = QLabel("GTIN")
        gtinprod = QLineEdit()
        self.codigo_gtin.setAlignment(Qt.AlignRight)

        layout = QHBoxLayout()
        layout.addWidget(self.codigo_produto)
        layout.addWidget(cdprod)

        layout.addWidget(self.codigo_ean)
        layout.addWidget(eanprod)

        layout.addWidget(self.codigo_gtin)
        layout.addWidget(gtinprod)

        layout.addWidget(self.uninput)

        layout.addStretch(1)
        self.GroupBox1.setLayout(layout)

    def createGroupBox(self):
        self.GroupBox2 = QGroupBox()

        self.label_descricao = QLabel("Descrição", self)
        self.label_descricao.setAlignment(Qt.AlignLeft)
        descricao = QLineEdit()
        descricao.setFixedSize(447, 25)

        self.label_custo = QLabel("Preço de Custo", self)
        self.label_custo.setAlignment(Qt.AlignLeft)
        precocusto = QLineEdit()
        precocusto.setFixedSize(107, 25)

        self.label_venda = QLabel("Preço de Venda", self)
        self.label_venda.setAlignment(Qt.AlignLeft)
        preco = QLineEdit()
        preco.setFixedSize(107, 25)

        layout = QVBoxLayout()

        layout.addWidget(self.label_descricao)
        layout.addWidget(descricao)

        layout.addWidget(self.label_custo)
        layout.addWidget(precocusto)

        layout.addWidget(self.label_venda)
        layout.addWidget(preco)

        layout.addStretch(1)
        self.GroupBox2.setLayout(layout)

    def createGroupBoxSalvar(self):
        self.GroupBox3 = QGroupBox("Salvar Cadastro")

        self.defaultPushButton = QPushButton("Salvar")
        self.defaultPushButton.setDefault(True)

        self.defaultPushButton.clicked.connect(self.addproduto)

        layout = QGridLayout()
        layout.addWidget(self.defaultPushButton, 1, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.GroupBox3.setLayout(layout)

    def addproduto(self):
        """
        captura as informações digitadas
        no lineedit e armazena nas variaveis
        :return:
        """
        descricao = ""
        ncm = ""
        un = ""
        preco = ""

        codigo_produto = self.cdprod.text()
        descricao = self.descricaoinput.text()
        ncm = self.eanprod.text()
        codgetin = self.gtinprod.text()
        un = self.uninput.itemText(self.uninput.currentIndex())
        preco = preco.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "INSERT INTO produtos (descricao, ncm, un, preco)" \
                          "VALUES (%s,%s,%s,%s)"
            dados = descricao, ncm, un, str(preco)
            self.cursor.execute(comando_sql, dados)
            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(
                QMessageBox(), 'Cadastro', 'Dados inseridos com sucesso!')
            self.close()

        except Exception:

            QMessageBox.warning(
                QMessageBox(), 'aleleonel@gmail.com', 'A inserção falhou!')


if __name__ == '__main__':
    appctxt = QApplication(sys.argv)
    gallery = CadastroProdutos()
    gallery.show()
    sys.exit(appctxt.exec())
