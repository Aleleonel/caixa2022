import os
import sys
import time
from datetime import date, datetime
from email import message
from unicodedata import decimal

import mysql.connector
from mysql.connector import OperationalError
from prettytable import PLAIN_COLUMNS, PrettyTable
from pyexpat import model
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QMessageBox, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)
from reportlab.pdfgen import canvas


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PEDIDOS")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

       

        self.Tables()
        self.show()
    
    def Tables(self):

        self.tableWidget = QTableView()

        
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)

        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        # self.tableWidget.setHorizontalHeaderLabels(
        #     ("Numero.Pedido", "Cod.Produto", "Descrição", "Quantidade", "total", "ultupdate",))


        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)

        lista = [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,89,0,11,1,1,2,67,67,54]
        
        self.tableWidget.setRowHeight(8,8)
        self.tableWidget.setColumnHidden(5, True)
    
        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.tableWidget)
        self.setLayout(self.vBox)


# class ListPedidos(QMainWindow):
    # def __init__(self):
    #     super(ListPedidos, self).__init__()
    #     self.setWindowIcon(QIcon('Icones/produtos.png'))

    #     self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PEDIDOS")
    #     self.setMinimumSize(800, 600)
    #     self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
    #     self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    #     # criar uma tabela centralizada
    #     self.tableWidget = QTableView()
    #     self.setCentralWidget(self.tableWidget)
    #     # muda a cor da linha selecionada
    #     self.tableWidget.setAlternatingRowColors(True)
    #     # indica a quantidade de colunas
    #     self.tableWidget.setColumnCount(6)
        # # define que o cabeçalho não seja alterado
        # self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        # self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # # Estica conforme o conteudo da célula
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # self.tableWidget.verticalHeader().setVisible(False)
        # self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        # self.tableWidget.verticalHeader().setStretchLastSection(False)
    #     self.tableWidget.setHorizontalHeaderLabels(
    #         ("Numero.Pedido", "Cod.Produto", "Descrição", "Quantidade", "total", "ultupdate",))

    #     self.cursor = conexao.banco.cursor()

    #     comando_sql = """ SELECT 
    #                         nr_caixa, 
    #                         cod_produto, 
    #                         p.descricao,
    #                         quantidade, 
    #                         valor_total,
    #                         ultupdate
    #                     FROM 
    #                         pedidocaixa 
    #                     LEFT JOIN produtos as p
    #                     ON cod_produto = p.codigo
    #                     order by 
    #                         ultupdate desc
    #                 """

    #     self.cursor.execute(comando_sql)
    #     result = self.cursor.fetchall()

    #     self.tableWidget.setRowCount(len(result))
    #     self.tableWidget.setColumnCount(6)

    #     for i in range(0, len(result)):
    #         for j in range(0, 6):
    #             self.tableWidget.setItem(
    #                 i, j, QTableWidgetItem(str(result[i][j])))

    #     toolbar = QToolBar()
    #     toolbar.setMovable(False)
    #     self.addToolBar(toolbar)

    #     statusbar = QStatusBar()
    #     self.setStatusBar(statusbar)
    #     # botões do menu

    #     btn_ac_refresch = QAction(
    #         QIcon("Icones/atualizar.png"), "Atualizar dados da Lista de Pedidos", self)
    #     btn_ac_refresch.triggered.connect(self.loaddatapedido)
    #     btn_ac_refresch.setStatusTip("Atualizar")
    #     toolbar.addAction(btn_ac_refresch)

    #     btn_ac_busca = QAction(
    #         QIcon("Icones/pesquisa.png"), "Filtra pedidos", self)
    #     btn_ac_busca.triggered.connect(self.filtraPedidos)
    #     btn_ac_busca.setStatusTip("Filtro")
    #     toolbar.addAction(btn_ac_busca)
        
    #     self.buscainput = QLineEdit()
    #     self.buscainput.textChanged.connect(self.filtraPedidos)
    #     toolbar.addWidget(self.buscainput)
   

    #     self.show()
    #     self.loaddatapedido()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
