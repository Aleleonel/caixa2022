import csv
import locale
import os
import sys
import time
from datetime import date, datetime
from decimal import Decimal
from email import message
from logging import warning
from operator import is_not
from sqlite3 import Cursor, Date
from unicodedata import decimal
from xml.etree.ElementTree import tostring

import mysql.connector
from fpdf import FPDF
from mysql.connector import OperationalError
from prettytable import PLAIN_COLUMNS, PrettyTable
from pyexpat import model
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

import conexao

global loginok


class ConsultaProdutosEstoque:
    def __init__(self):
        self.cursor = conexao.banco.cursor()

    def consultar_produtos(self):
        """Consulta produtos na hora da venda, tras apenas itens com saldo em estoque"""
        consulta_prod = """SELECT p.codigo, p.descricao, p.preco, p.ncm, p.un, p.status FROM produtos as p
                            inner join controle_clientes.estoque as e
                            where e.status = '{}'
                            and e.estoque > '{}'
                            and p.status = '{}'
                            and e.idproduto = p.codigo group by p.codigo""".format(
            "E", 0, 1
        )

        self.cursor.execute(consulta_prod)
        result_prod = self.cursor.fetchall()
        self.cursor.close()

        # Criação da lista de produtos
        produtos = [item[1] for item in result_prod if item[1]]

        return produtos

    def consultar_produtos_geral(self):
        """Consulta produtos na hora da venda, traz apenas um item com saldo em estoque por código de produto"""
        consulta_prod = """SELECT p.codigo, MAX(p.descricao) as descricao, p.preco, 
                    MAX(e.preco_compra) as preco_compra, p.ncm, p.un 
                    FROM produtos as p
                    LEFT JOIN controle_clientes.estoque as e
                    ON p.codigo = e.idproduto
                    GROUP BY p.codigo, p.preco, p.ncm, p.un"""

        self.cursor.execute(consulta_prod)
        result_prod = self.cursor.fetchall()
        self.cursor.close()

        # Criação da lista de produtos
        produtos_geral = [item[1] for item in result_prod if item[1]]

        return produtos_geral

    def consultaProdutosLista(self, consulta):
        """Consulta todos os itens cadastrados pela descrição para uma simples consulta"""
        try:
            self.cursor = conexao.banco.cursor()

            sql = """SELECT p.codigo, p.descricao, MAX(p.preco) as preco, MAX(p.ncm) as ncm, MAX(p.un) as un, MAX(e.preco_compra) as preco_compra
                    FROM produtos as p
                    INNER JOIN controle_clientes.estoque as e
                    ON p.codigo = e.idproduto
                    """

            where = f" WHERE descricao = '{consulta}' GROUP BY p.codigo"  # AND est.idproduto = codigo
            comando_sql = sql + where
            self.cursor.execute(comando_sql)
            result = self.cursor.fetchall()
            self.cursor.close()

            if not result:
                raise Exception(
                    "Produto não cadastrado ou sem movimentação em estoque!"
                )

            return result

        except Exception as e:
            raise e  # Lança a exceção para ser tratada na classe filha

    def consultaCodigoslista(self, consultacodigo):
        """Consulta todos os itens cadastrados pelo código para uma simples consulta"""
        try:
            self.cursor = conexao.banco.cursor()
            sql = "SELECT codigo, descricao, ncm, un, preco, est.preco_compra \
                   FROM produtos \
                   inner join controle_clientes.estoque as est"

            where = f" WHERE codigo = '{consultacodigo}' "  # AND est.idproduto = codigo
            comando_sql = sql + where
            self.cursor.execute(comando_sql)
            result = self.cursor.fetchall()
            self.cursor.close()

            if not result:
                raise Exception(
                    "Produto não cadastrado ou sem movimentação em estoque!"
                )

            return result

        except Exception as e:
            raise e  # Lança a exceção para ser tratada na classe filha


class AboutDialog(QDialog):
    """
    Define uma nova janela onde mostra as informações
    do botão sobre
    """

    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(500)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Configurações do titulo da Janela
        layout = QVBoxLayout()

        self.setWindowTitle("Sobre")
        title = QLabel("SCC - Sistema de Controle de Clientes")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        # Configurações de atribuição de imagem
        labelpic = QLabel()
        pixmap = QPixmap("Icones/perfil.png")
        # pixmap = pixmap.scaledToWidth(400)
        pixmap = pixmap.scaled(QSize(500, 500))
        labelpic.setPixmap(pixmap)
        # labelpic.setFixedHeight(400)
        layout.addWidget(title)
        layout.addWidget(labelpic)

        layout.addWidget(QLabel("Versão:V1.0"))
        layout.addWidget(QLabel("Nome: Alexandre Leonel de Oliveira"))
        layout.addWidget(QLabel("Nascido em: São Paulo em 26 de Junho de 1974"))
        layout.addWidget(QLabel("Profissão: Bacharel em Sistemas de Informação"))
        layout.addWidget(QLabel("Copyright Bi-Black-info 2021"))

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


class CadastroEstoque(QDialog):
    def __init__(self, *args, **kwargs):
        super(CadastroEstoque, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(300)

        self.carrega_produtos()

        self.QBtn = QPushButton("Registrar")
        self.QBtn_close = QPushButton("Cancelar")
        self.setWindowTitle("Adicionar Estoque")

        layout = QVBoxLayout()
        layout.addWidget(self.codigoinput)

        self.statusinput = QLineEdit()
        self.statusinput.setPlaceholderText("E")
        self.statusinput.setReadOnly(True)
        layout.addWidget(self.statusinput)

        self.descricaoinput = QLineEdit()
        self.descricaoinput.setPlaceholderText("Descrição")
        self.descricaoinput.setReadOnly(True)
        layout.addWidget(self.descricaoinput)

        self.precoinput = QLineEdit()
        self.precoinput.setPlaceholderText("Preço de Compra")
        layout.addWidget(self.precoinput)

        self.qtdinput = QLineEdit()
        self.qtdinput.setPlaceholderText("Quantidade")
        layout.addWidget(self.qtdinput)

        layout.addWidget(self.QBtn)
        layout.addWidget(self.QBtn_close)
        self.setLayout(layout)

        self.codigoinput.currentIndexChanged.connect(self.carrega_descricao_saldo)
        self.QBtn.clicked.connect(self.addproduto)
        self.QBtn_close.clicked.connect(self.cancelar)

    def carrega_produtos(self):
        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql = "SELECT * FROM produtos"
            self.cursor.execute(consulta_sql)
            result = self.cursor.fetchall()

            self.codigoinput = QComboBox()
            for row in result:
                self.codigoinput.addItem(str(row[0]))
        except Exception as e:
            QMessageBox.warning(QMessageBox(), "Erro na Busca", str(e))

    def carrega_descricao_saldo(self):
        try:
            codigo = self.codigoinput.currentText()
            self.cursor = conexao.banco.cursor()
            consulta_sql = "SELECT descricao FROM produtos WHERE codigo = %s"
            self.cursor.execute(consulta_sql, (codigo,))
            valor_codigo = self.cursor.fetchone()

            if valor_codigo:
                self.descricaoinput.setText(valor_codigo[0])
            else:
                self.descricaoinput.clear()
        except Exception as e:
            QMessageBox.warning(QMessageBox(), "Erro na Inserção", str(e))

    def addproduto(self):
        codigo = self.codigoinput.currentText()
        quantidade = self.qtdinput.text()
        preco = self.precoinput.text()
        status = "E"
        # descricao = self.descricaoinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = (
                "INSERT INTO estoque (idproduto, estoque, status, preco_compra)"
                "VALUES (%s, %s, %s, %s)"
            )
            dados = (codigo, quantidade, status, preco)
            self.cursor.execute(comando_sql, dados)
            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(
                QMessageBox(), "Cadastro", "Dados inseridos com sucesso!"
            )
            self.close()

        except Exception as e:
            QMessageBox.warning(QMessageBox(), "Erro na Inserção", str(e))

    def cancelar(self):
        self.hide()


class ListEstoque(QMainWindow):
    def __init__(self):
        super(ListEstoque, self).__init__()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE ESTOQUE")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(6)
        # define que o cabeçalho não seja alterado
        # self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        # self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        # Estica conforme o conteudo da célula
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.ResizeToContents
        )

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Codigo",
                "Itens",
                "Entradas",
                "Saidas",
                "Saldo",
            )
        )

        # self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.cursor = conexao.banco.cursor()
        comando_sql = """
                      select
                        idproduto,
                        p.descricao,
                        coalesce(
                            (SELECT
                                sum(e.estoque) entrada
                             FROM estoque e
                             where status = 'E'
                             and e.idproduto = i.idproduto), 0) entrada,
                        coalesce(
                            (SELECT
                                sum(e.estoque) saida
                             FROM estoque e
                             where status = 'S'
                             and e.idproduto = i.idproduto), 0) saida,

                          coalesce(
                              ((SELECT
                                 sum(e.estoque) entrada
                               FROM estoque e
                               where status = 'E'
                               and e.idproduto = i.idproduto) -
                              (SELECT
                                 sum(e.estoque) saida
                               FROM estoque e
                               where status = 'S'
                               and e.idproduto = i.idproduto)), 0) estoque

                      from
                         estoque i
                      inner join produtos p on p.codigo = i.idproduto
                      group by
                         idproduto
        """
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("Icones/add.png"), "Cadastro Estoque", self)
        btn_ac_adduser.triggered.connect(self.cadEstoque)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(
            QIcon("Icones/atualizar.png"), "Atualizar dados do Estoque", self
        )
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(
            QIcon("Icones/pesquisa.png"), "Pesquisar Produtos em Estoque", self
        )
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_sair = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_sair.triggered.connect(self.fechar)
        toolbar.addAction(btn_ac_sair)

        # self.show()
        self.showFullScreen()

    def loaddata(self):
        self.cursor = conexao.banco.cursor()
        comando_sql = """
                             select
                               idproduto,
                               p.descricao,
                               coalesce(
                                   (SELECT
                                       sum(e.estoque) entrada
                                    FROM estoque e
                                    where status = 'E'
                                    and e.idproduto = i.idproduto), 0) entrada,
                               coalesce(
                                   (SELECT
                                       sum(e.estoque) saida
                                    FROM estoque e
                                    where status = 'S'
                                    and e.idproduto = i.idproduto), 0) saida,

                                 coalesce(
                                     ((SELECT
                                        sum(e.estoque) entrada
                                      FROM estoque e
                                      where status = 'E'
                                      and e.idproduto = i.idproduto) -
                                     (SELECT
                                        sum(e.estoque) saida
                                      FROM estoque e
                                      where status = 'S'
                                      and e.idproduto = i.idproduto)), 0) estoque

                             from
                                estoque i
                             inner join produtos p on p.codigo = i.idproduto
                             group by
                                idproduto
               """
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadEstoque(self):
        dlg = CadastroEstoque()
        dlg.exec()
        self.loaddata()

    def search(self):
        dlg = SearchEstoque()
        dlg.exec_()

    def fechar(self):
        self.close()


class SearchEstoque(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchEstoque, self).__init__(*args, **kwargs)

        self.cursor = conexao.banco.cursor()
        self.current_record = 0
        self.result_estoque = []
        self.result_produto = []

        self.setWindowTitle("Pesquisar Produto em Estoque")
        self.setFixedSize(600, 400)

        # Widgets
        self.product_name_label = QLabel(
            "Descrição do Produto"
        )  # Texto padrão como marcador de espaço
        self.product_name_label.setAlignment(Qt.AlignCenter)
        self.product_name_label.setStyleSheet(
            "font-size: 18px; background-color: #f0f0f0;"
        )  # Estilo com cor de fundo cinza
        self.product_name_label.setFixedHeight(40)

        self.searchinput = QLineEdit()
        self.searchinput.setValidator(QIntValidator())
        self.searchinput.setPlaceholderText("Código...")
        self.search_btn = QPushButton("Procurar")

        self.close_btn = QPushButton("Fechar")

        self.result_label = QLabel("Código:")
        self.description_label = QLabel("Descrição:")
        self.entrada_label = QLabel("Quantidade de Entrada:")
        self.saida_label = QLabel("Quantidade de Saída:")
        self.saldo_label = QLabel("Saldo:")

        self.result_lineedit = QLineEdit()
        self.description_lineedit = QLineEdit()
        self.entrada_lineedit = QLineEdit()
        self.saida_lineedit = QLineEdit()
        self.saldo_lineedit = QLineEdit()

        for widget in [
            self.result_lineedit,
            self.description_lineedit,
            self.entrada_lineedit,
            self.saida_lineedit,
            self.saldo_lineedit,
        ]:
            widget.setReadOnly(True)
            widget.setStyleSheet("background-color: #f0f0f0;")  # Cor de fundo cinza

        # Layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Código do Produto:"), 0, 0)
        grid_layout.addWidget(self.searchinput, 0, 1)
        grid_layout.addWidget(self.search_btn, 0, 2)
        grid_layout.addWidget(self.close_btn, 1, 2)

        grid_layout.addWidget(self.result_label, 1, 0)
        grid_layout.addWidget(self.result_lineedit, 1, 1)
        grid_layout.addWidget(self.description_label, 2, 0)
        grid_layout.addWidget(self.description_lineedit, 2, 1)
        grid_layout.addWidget(self.entrada_label, 3, 0)
        grid_layout.addWidget(self.entrada_lineedit, 3, 1)
        grid_layout.addWidget(self.saida_label, 4, 0)
        grid_layout.addWidget(self.saida_lineedit, 4, 1)
        grid_layout.addWidget(self.saldo_label, 5, 0)
        grid_layout.addWidget(self.saldo_lineedit, 5, 1)

        nav_layout = QHBoxLayout()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.product_name_label)
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)

        self.search_btn.clicked.connect(self.searchProdEstoque)
        self.close_btn.clicked.connect(self.prodEstoqueclose)

    def searchProdEstoque(self):
        searchroll = self.searchinput.text()
        try:
            comando_sql = """
              select
                idproduto,
                p.descricao,
                coalesce(
                    (SELECT
                        sum(e.estoque) entrada
                     FROM estoque e
                     where status = 'E'
                     and e.idproduto = i.idproduto), 0) entrada,
                coalesce(
                    (SELECT
                        sum(e.estoque) saida
                     FROM estoque e
                     where status = 'S'
                     and e.idproduto = i.idproduto), 0) saida,

                  coalesce(
                      ((SELECT
                         sum(e.estoque) entrada
                       FROM estoque e
                       where status = 'E'
                       and e.idproduto = i.idproduto) -
                      (SELECT
                         sum(e.estoque) saida
                       FROM estoque e
                       where status = 'S'
                       and e.idproduto = i.idproduto)), 0) estoque

              from
                 estoque i
              inner join produtos p on p.codigo = i.idproduto
              where idproduto = %s
            """
            self.cursor.execute(comando_sql, (searchroll,))
            result = self.cursor.fetchall()
            self.result_estoque = result
            self.current_record = 0
            self.showRecord()

        except Exception as e:
            QMessageBox.warning(self, "Pesquisa falhou", str(e))

    def showRecord(self):
        if self.result_estoque:
            estoque_record = self.result_estoque[self.current_record]

            self.product_name_label.setText(
                estoque_record[1]
            )  # Atualize o rótulo do nome do produto
            self.result_lineedit.setText(str(estoque_record[0]))
            self.description_lineedit.setText(estoque_record[1])
            self.entrada_lineedit.setText(str(estoque_record[2]))
            self.saida_lineedit.setText(str(estoque_record[3]))
            self.saldo_lineedit.setText(str(estoque_record[4]))

    def prodEstoqueclose(self):
        self.hide()


class SearchClientes(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchClientes, self).__init__(*args, **kwargs)

        self.editDialog = None  # Variável para armazenar o EditDialog

        self.setGeometry(
            100, 100, 800, 600
        )  # Define a posição e tamanho inicial da janela

        self.createTopLeftGroupBox()
        self.createGroupBoxSalvar()
        self.createGroupBox()
        self.createEndercoGroupBox()
        self.buscaregistros()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox1, 1, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox2, 2, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox3, 4, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox4, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("BUSCA POR CLIENTES")

    def createGroupBox(self):
        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "SELECT * FROM clientes"

            self.cursor.execute(comando_sql)
            result = self.cursor.fetchall()

            clientes = []
            for i in range(len(result)):
                if result[i][2]:
                    clientes.append(result[i][2])

        except Exception as e:
            QMessageBox.warning(
                QMessageBox(), "Erro", f"A busca de registros falhou: {str(e)}"
            )

        self.GroupBox2 = QGroupBox()

        layout = QVBoxLayout()

        # Crie um QFormLayout para os pares de rótulos e QLineEdit
        form_layout = QFormLayout()

        self.checkbox = QCheckBox("Ativo")
        self.checkbox.setChecked(True)  # Inicialmente definido como ativo
        form_layout.addRow("Status:", self.checkbox)

        self.rasao = QLineEdit()
        self.rasao.setPlaceholderText("Nome / Razão: ")
        self.model = QStandardItemModel()
        self.model = clientes
        completer = QCompleter(self.model, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.rasao.setCompleter(completer)
        self.rasao.editingFinished.connect(self.buscaregistro)
        self.rasao.setFocus(True)
        form_layout.addRow("Nome / Razão: ", self.rasao)

        self.rginput = QLineEdit()
        self.rginput.setPlaceholderText("R.G")
        form_layout.addRow("RG:", self.rginput)

        self.cpfinput = QLineEdit()
        self.cpfinput.setPlaceholderText("CPF")
        form_layout.addRow("CPF.:", self.cpfinput)

        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Telefone NO.")
        self.mobileinput.setReadOnly(True)
        form_layout.addRow("Telefone NO.:", self.mobileinput)

        # Adicione uma instância do modelo de dados
        self.headers = [
            "Tipo",
            "Nome / Razão",
            "RG",
            "CPF",
            "Telefone",
            "Endereço",
            "Bairro",
            "Complemento",
            "Nr.",
            "CEP",
            "Cidade",
        ]
        self.model = ClientTableModel([], self.headers)
        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # layout.addWidget(self.tableView)

        # Adicione o QFormLayout ao layout vertical
        layout.addLayout(form_layout)

        layout.addStretch(1)
        self.GroupBox2.setLayout(layout)

        self.checkbox.stateChanged.connect(self.alterarStatus)

    def createTopLeftGroupBox(self):
        self.GroupBox1 = QGroupBox("Clientes")

        layout = QVBoxLayout()

        # Crie um QFormLayout para os pares de rótulos e QLineEdit

        self.nameinput = QLineEdit()
        self.nameinput.setMaxLength(30)  # Define o comprimento máximo
        self.nameinput.setMinimumWidth(200)
        self.nameinput.setPlaceholderText("Tipo")
        self.nameinput.setReadOnly(True)
        layout.addWidget(self.nameinput)

        layout.addLayout(layout)

        layout.addStretch(1)
        self.GroupBox1.setLayout(layout)

    def createEndercoGroupBox(self):
        self.GroupBox4 = QGroupBox()
        layout = QVBoxLayout()

        # Crie um QFormLayout para os pares de rótulos e QLineEdit
        form_layout = QFormLayout()

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Logradouro")
        self.addressinput.setReadOnly(True)
        form_layout.addRow("Logradouro:", self.addressinput)

        self.bairro = QLineEdit()
        self.bairro.setPlaceholderText("Bairro")
        self.bairro.setReadOnly(True)
        form_layout.addRow("Bairro:", self.bairro)

        self.addresscomplemento = QLineEdit()
        self.addresscomplemento.setPlaceholderText("Complemento")
        self.addresscomplemento.setReadOnly(True)
        form_layout.addRow("Complemento:", self.addresscomplemento)

        self.addresscidade = QLineEdit()
        self.addresscidade.setPlaceholderText("Cidade")
        self.addresscidade.setReadOnly(True)
        form_layout.addRow("Cidade:", self.addresscidade)

        self.cep = QLineEdit()
        self.cep.setPlaceholderText("CEP")
        self.cep.setReadOnly(True)
        form_layout.addRow("CEP.:", self.cep)

        self.ederecoNumero = QLineEdit()
        self.ederecoNumero.setPlaceholderText("Nr.")
        self.ederecoNumero.setReadOnly(True)
        form_layout.addRow("Nr.:", self.ederecoNumero)

        layout.addLayout(form_layout)

        layout.addStretch(1)
        self.GroupBox4.setLayout(layout)

    def createGroupBoxSalvar(self):
        self.GroupBox3 = QGroupBox("Registro")

        # Adicione botões para avançar e voltar
        self.nextButton = QPushButton("Próximo")
        self.prevButton = QPushButton("Anterior")
        self.firstButton = QPushButton("Primeiro")
        self.lastButton = QPushButton("Último")

        self.nextButton.clicked.connect(self.avancarRegistro)
        self.prevButton.clicked.connect(self.voltarRegistro)
        self.firstButton.clicked.connect(self.voltarPrimeiroRegistro)
        self.lastButton.clicked.connect(self.avancarUltimoRegistro)

        self.editButton = QPushButton("Editar")
        self.editButton.clicked.connect(self.editarRegistro)

        self.defaultPushButton2 = QPushButton(self)
        self.defaultPushButton2.setIcon(QIcon("Icones/sair.png"))
        self.defaultPushButton2.clicked.connect(self.closeCadastro)

        layout = QGridLayout()

        # Modifique a disposição dos botões
        layout.addWidget(self.editButton, 1, 0)
        layout.addWidget(self.firstButton, 2, 0)
        layout.addWidget(self.prevButton, 2, 1)
        layout.addWidget(self.nextButton, 2, 2)
        layout.addWidget(self.lastButton, 2, 3)
        layout.addWidget(self.defaultPushButton2, 1, 1)
        layout.setRowStretch(5, 1)
        self.GroupBox3.setLayout(layout)

        # Inicializa uma variável para rastrear o índice do registro atual
        self.current_record_index = 0
        self.records = []

    def buscaregistro(self):
        try:
            self.cursor = conexao.banco.cursor()
            valor = self.rasao.text()

            comando_sql = "SELECT * FROM clientes WHERE nome LIKE %s"
            valor_busca = f"%{valor}%"

            self.cursor.execute(comando_sql, (valor_busca,))
            result = self.cursor.fetchall()
            self.cursor.close()

            self.records = [item for item in result if item]
            self.current_record_index = 0

            if not self.records:
                QMessageBox.information(
                    self, "Informação", "Nenhum registro encontrado para a pesquisa."
                )

            # Atualiza os campos com base no registro atual
            self.atualizarCampos()

            # Atualiza a habilitação dos botões de navegação
            self.updateNavigationButtons()

        except Exception as e:
            QMessageBox.warning(
                QMessageBox(), "Erro", f"A busca de registros falhou: {str(e)}"
            )

    def buscaregistros(self):
        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "SELECT * FROM clientes"

            self.cursor.execute(comando_sql)
            result = self.cursor.fetchall()
            self.cursor.close()

            # Atualiza o modelo de dados com os registros obtidos
            self.records = [item for item in result if item]
            self.model = ClientTableModel(self.records, self.headers)
            self.tableView.setModel(self.model)
            self.current_record_index = 0

            # Atualiza os campos com base no registro atual
            self.atualizarCampos()

        except Exception as e:
            QMessageBox.warning(
                QMessageBox(), "Erro", f"A busca de registros falhou: {str(e)}"
            )

    def updateNavigationButtons(self):
        num_records = len(self.records)
        if num_records == 0:
            self.firstButton.setEnabled(False)
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(False)
            self.lastButton.setEnabled(False)
        elif self.current_record_index == 0:
            self.firstButton.setEnabled(False)
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
            self.lastButton.setEnabled(True)
        elif self.current_record_index == num_records - 1:
            self.firstButton.setEnabled(True)
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
            self.lastButton.setEnabled(False)
        else:
            self.firstButton.setEnabled(True)
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)
            self.lastButton.setEnabled(True)

    def avancarRegistro(self):
        if self.current_record_index < len(self.records) - 1:
            self.current_record_index += 1
            self.atualizarCampos()
            self.updateNavigationButtons()

    def voltarRegistro(self):
        if self.current_record_index > 0:
            self.current_record_index -= 1
            self.atualizarCampos()
            self.updateNavigationButtons()

    def avancarUltimoRegistro(self):
        if len(self.records) > 0:
            self.current_record_index = len(self.records) - 1
            self.atualizarCampos()
            self.updateNavigationButtons()

    def voltarPrimeiroRegistro(self):
        if len(self.records) > 0:
            self.current_record_index = 0
            self.atualizarCampos()
            self.updateNavigationButtons()

    def atualizarCampos(self):
        if 0 <= self.current_record_index < len(self.records):
            # Atualizar os campos com base no registro atual
            record = self.records[self.current_record_index]

            self.nameinput.setText(record[1])
            self.rasao.setText(record[2])
            self.cpfinput.setText(record[4])
            self.rginput.setText(record[3])

            self.mobileinput.setText(record[5])
            self.addressinput.setText(record[6])
            self.bairro.setText(record[8])

            self.addresscomplemento.setText(record[7])
            self.ederecoNumero.setText(record[9])
            self.cep.setText(record[10])
            self.addresscidade.setText(record[11])

            # Atualize o status do checkbox com base no registro atual
            self.checkbox.setChecked(bool(record[13]))

            # Atualize a habilitação dos botões de navegação
            self.updateNavigationButtons()

    def editarRegistro(self):
        self.atualizarCampos()
        if self.current_record_index < len(self.records):
            # Obtenha o registro atual
            record = self.records[self.current_record_index]

            # Crie uma instância de EditDialog e atribua-a a self.editDialog
            self.editDialog = EditDialog(record)

            # Conecte um sinal para atualizar os dados após a edição ser concluída
            self.editDialog.edicaoConcluida.connect(self.atualizarRegistroEditado)

            # Exiba a janela de edição
            self.editDialog.exec_()

    def alterarStatus(self):
        if 0 <= self.current_record_index < len(self.records):
            cursor = conexao.banco.cursor()

            novo_status = (
                1 if self.checkbox.isChecked() else 0
            )  # 1 para ativo, 0 para inativo

            query = (
                "UPDATE controle_clientes.clientes SET status = %s WHERE codigo = %s"
            )
            # Supondo que você tenha uma coluna 'id' como identificador
            id_registro = self.records[self.current_record_index][
                0
            ]  # Obtém o ID do registro atual

            cursor.execute(query, (novo_status, id_registro))
            conexao.banco.commit()

    def atualizarRegistroEditado(self):
        # Atualize os campos na janela principal após a edição
        self.atualizarCampos()

    def closeCadastro(self):
        self.close()


class EditDialog(QDialog):
    edicaoConcluida = pyqtSignal()

    def __init__(self, record, parent=None):
        super(EditDialog, self).__init__(parent)
        self.record = record
        self.initUI()

    def initUI(self):
        self.setGeometry(
            100, 100, 800, 600
        )  # Define a posição e tamanho inicial da janela

        layout = QVBoxLayout()

        # Crie um QFormLayout para os pares de rótulos e QLineEdit
        form_layout = QFormLayout()

        self.tipo = QLineEdit(self.record[1])
        self.tipo.setMaxLength(30)  # Define o comprimento máximo
        self.tipo.setMinimumWidth(30)
        self.tipo.setPlaceholderText("Tipo")
        self.tipo.setReadOnly(True)
        form_layout.addRow("Tipo.:", self.tipo)

        self.razao = QLineEdit(self.record[2])
        self.razao.setPlaceholderText("Nome / Razão: ")
        form_layout.addRow("Nome / Razão: ", self.razao)

        self.rginput = QLineEdit(self.record[3])
        self.rginput.setPlaceholderText("R.G")
        form_layout.addRow("RG:", self.rginput)

        self.cpfinput = QLineEdit(self.record[4])
        self.cpfinput.setPlaceholderText("CPF")
        form_layout.addRow("CPF.:", self.cpfinput)

        self.mobileinput = QLineEdit(self.record[5])
        self.mobileinput.setPlaceholderText("Telefone NO.")
        form_layout.addRow("Telefone NO.:", self.mobileinput)

        self.addressinput = QLineEdit(self.record[6])
        self.addressinput.setPlaceholderText("Endereço")
        form_layout.addRow("Endereço:", self.addressinput)

        self.bairro = QLineEdit(self.record[8])
        self.bairro.setPlaceholderText("Bairro")
        form_layout.addRow("Bairro:", self.bairro)

        self.addresscomplemento = QLineEdit(self.record[7])
        self.addresscomplemento.setPlaceholderText("Complemento")
        form_layout.addRow("Complemento:", self.addresscomplemento)

        self.addresscidade = QLineEdit(self.record[11])
        self.addresscidade.setPlaceholderText("Cidade")
        form_layout.addRow("Cidade:", self.addresscidade)

        self.cep = QLineEdit(self.record[10])
        self.cep.setPlaceholderText("CEP")
        form_layout.addRow("CEP.:", self.cep)

        self.ederecoNumero = QLineEdit(self.record[9])
        self.ederecoNumero.setPlaceholderText("Nr.")
        form_layout.addRow("Nr.:", self.ederecoNumero)

        # Adicione um botão para salvar as alterações
        saveButton = QPushButton("Salvar Alterações")
        saveButton.clicked.connect(self.salvarAlteracoes)
        form_layout.addRow(saveButton)

        layout.addLayout(form_layout)
        layout.addStretch(1)
        self.setLayout(layout)

    def salvarAlteracoes(self):
        # Obtenha os novos dados dos campos de edição
        tipo = self.tipo.text()
        razao = self.razao.text()
        rg = self.rginput.text()
        cpf = self.cpfinput.text()

        telefone = self.mobileinput.text()
        endereco = self.addressinput.text()
        bairro = self.bairro.text()

        complemento = self.addresscomplemento.text()
        enderecoNumero = self.ederecoNumero.text()
        cep = self.cep.text()
        cidade = self.addresscidade.text()

        try:
            self.cursor = conexao.banco.cursor()

            # Execute uma instrução SQL para atualizar o campo específico
            sql = f"UPDATE controle_clientes.clientes SET tipo = %s, nome = %s, cpf = %s,  rg = %s, telefone = %s, endereco = %s, bairro = %s, complemento = %s, numero = %s, cep = %s, cidade = %s WHERE codigo = %s"
            valores = (
                tipo,
                razao,
                cpf,
                rg,
                telefone,
                endereco,
                bairro,
                complemento,
                enderecoNumero,
                cep,
                cidade,
                self.record[0],
            )
            self.cursor.execute(sql, valores)

            # Faça commit das alterações no banco de dados
            conexao.banco.commit()

            # Emita um sinal para indicar que a edição foi concluída
            self.edicaoConcluida.emit()

            # Feche a janela de edição
            self.accept()

        except Exception as e:
            QMessageBox.warning(
                QMessageBox(), "Erro", f"Não foi possível alterar os campos: {str(e)}"
            )


class ClientTableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super(ClientTableModel, self).__init__(parent)
        self.data = data
        self.headers = headers

    def rowCount(self, parent=Qt.DisplayRole):
        return len(self.data)

    def columnCount(self, parent=Qt.DisplayRole):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.data[row][col])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None


class EditProdutosDialog(QDialog):
    edicaoConcluida = pyqtSignal()

    def __init__(self, record, parent=None):
        super(EditProdutosDialog, self).__init__(parent)
        self.record = record
        self.initUI()

    def initUI(self):
        self.setGeometry(
            100, 100, 800, 600
        )  # Define a posição e tamanho inicial da janela

        self.createTopLeftGroupBox()
        self.createGroupBoxSalvar()
        self.createGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

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

        self.setWindowTitle("EDITAR PRODUTOS")

    def createTopLeftGroupBox(self):
        self.GroupBox1 = QGroupBox("Edição de Itens")
        # Crie um QFormLayout para os pares de rótulos e QLineEdit
        form_layout = QFormLayout()
        layout = QHBoxLayout()

        # Insere o ramo ou tipo  /
        # Criar uma tabela para cadastrar unidade de medida
        self.uninput = QComboBox()
        self.uninput.addItem("UN")
        self.uninput.addItem("PÇ")
        self.uninput.addItem("KG")
        self.uninput.addItem("LT")
        self.uninput.addItem("PT")
        self.uninput.addItem("CX")

        self.cdprod = QLineEdit(str(self.record[0]))
        self.cdprod.setAlignment(Qt.AlignLeft)
        self.cdprod.setFixedSize(107, 25)
        form_layout.addRow("Codigo.:", self.cdprod)

        self.eanprod = QLineEdit(str(self.record[3]))
        self.eanprod.setFixedSize(107, 25)
        form_layout.addRow("EAN.:", self.eanprod)

        self.gtinprod = QLineEdit()
        self.gtinprod.setFixedSize(107, 25)
        form_layout.addRow("GTIN.:", self.gtinprod)

        # layout.addStretch(1)
        layout.addLayout(form_layout)
        self.GroupBox1.setLayout(layout)

    def createGroupBox(self):
        self.GroupBox2 = QGroupBox()

        self.label_descricao = QLabel("Descrição", self)
        self.label_descricao.setAlignment(Qt.AlignLeft)
        self.descricao = QLineEdit(str(self.record[1]))
        self.descricao.setFixedSize(447, 25)

        self.label_custo = QLabel("Preço de Custo", self)
        self.label_custo.setAlignment(Qt.AlignLeft)
        self.precocusto = QLineEdit(str(self.record[6]))
        self.precocusto.setFixedSize(107, 25)

        self.label_venda = QLabel("Preço de Venda", self)
        self.label_venda.setAlignment(Qt.AlignLeft)
        self.preco = QLineEdit(str(self.record[2]))
        self.preco.setFixedSize(107, 25)

        self.label_unidade = QLabel("Un. de Medida", self)
        self.uninput.setFixedSize(107, 25)

        layout = QVBoxLayout()

        layout.addWidget(self.label_descricao)
        layout.addWidget(self.descricao)

        layout.addWidget(self.label_custo)
        layout.addWidget(self.precocusto)

        layout.addWidget(self.label_venda)
        layout.addWidget(self.preco)

        layout.addWidget(self.label_unidade)
        layout.addWidget(self.uninput)

        layout.addStretch(1)
        self.GroupBox2.setLayout(layout)

    def createGroupBoxSalvar(self):
        self.GroupBox3 = QGroupBox("Salvar Cadastro")

        self.defaultPushButton = QPushButton("Salvar")
        self.defaultPushButton.setDefault(True)
        self.defaultPushButton.clicked.connect(self.salvarAlteracoes)

        self.defaultPushButton2 = QPushButton("Fechar")
        self.defaultPushButton2.setDefault(True)
        self.defaultPushButton2.clicked.connect(self.closeCadastro)

        layout = QGridLayout()
        layout.addWidget(self.defaultPushButton, 1, 0, 1, 2)
        layout.addWidget(self.defaultPushButton2, 2, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.GroupBox3.setLayout(layout)

    def salvarAlteracoes(self):
        # Obtenha os novos dados dos campos de edição

        descricao = self.descricao.text()
        preco = self.preco.text()
        ncm = self.eanprod.text()
        un = self.uninput.currentText()

        # Atualiza os campos na janela principal após a edição
        self.record = (
            self.record[0],
            descricao,
            preco,
            ncm,
            un,
        )

        # alterações necessárias no registro
        try:
            self.cursor = conexao.banco.cursor()
            # Execute uma instrução SQL para atualizar o campo específico
            sql = f"UPDATE controle_clientes.produtos SET descricao = %s, preco = %s, ncm = %s,  un = %s WHERE codigo = %s"
            valores = (
                descricao,
                preco,
                ncm,
                un,
                self.record[0],
            )
            self.cursor.execute(sql, valores)

            # Faça commit das alterações no banco de dados
            conexao.banco.commit()

            # Emita um sinal para indicar que a edição foi concluída
            self.edicaoConcluida.emit()

            # Feche a janela de edição
            self.accept()

        except Exception as e:
            QMessageBox.warning(
                QMessageBox(), "Erro", f"Não foi possível alterar os campos: {str(e)}"
            )

    def closeCadastro(self):
        self.close()


class ProdutoTableModel(QAbstractTableModel):
    def __init__(self, data, headers, parent=None):
        super(ProdutoTableModel, self).__init__(parent)
        self.data = data
        self.headers = headers

    def rowCount(self, parent=Qt.DisplayRole):
        return len(self.data)

    def columnCount(self, parent=Qt.DisplayRole):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.data[row][col])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None


class CadastroClientes(QDialog):
    def __init__(self, *args, **kwargs):
        super(CadastroClientes, self).__init__(*args, **kwargs)

        self.setGeometry(
            100, 100, 800, 600
        )  # Define a posição e tamanho inicial da janela

        self.createTopLeftGroupBox()
        self.createGroupBoxSalvar()
        self.createGroupBox()
        self.createEndercoGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox1, 1, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox2, 2, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox3, 4, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox4, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("CADASTRO DE CLIENTES")

    def createGroupBox(self):
        self.GroupBox2 = QGroupBox()
        layout = QHBoxLayout()
        form_layout = QFormLayout()

        self.cpfinput = QLineEdit()
        self.cpfinput.setPlaceholderText("CPF")
        form_layout.addRow("CPF.:", self.cpfinput)

        self.rginput = QLineEdit()
        self.rginput.setPlaceholderText("R.G")
        form_layout.addRow("RG.:", self.rginput)

        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Telefone NO.")
        form_layout.addRow("Telefone NO.", self.mobileinput)

        layout.addLayout(form_layout)
        layout.addStretch(1)
        self.GroupBox2.setLayout(layout)

    def createTopLeftGroupBox(self):
        self.GroupBox1 = QGroupBox("Cadastro de Clientes")
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Insere o ramo ou tipo /
        self.branchinput = QComboBox()
        self.branchinput.addItem("Pessoa Física")
        self.branchinput.addItem("Pessoa Jurídica")
        form_layout.addRow("Tipo.:", self.branchinput)

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Nome / Razão")
        form_layout.addRow("Nome / Razão", self.nameinput)

        layout.addStretch(1)
        layout.addLayout(form_layout)
        self.GroupBox1.setLayout(layout)

    def createEndercoGroupBox(self):
        self.GroupBox4 = QGroupBox()
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Logradouro")
        form_layout.addRow("Endereço", self.addressinput)

        self.bairro = QLineEdit()
        self.bairro.setPlaceholderText("Bairro")
        form_layout.addRow("Bairro", self.bairro)

        self.addresscomplemento = QLineEdit()
        self.addresscomplemento.setPlaceholderText("Complemento")
        form_layout.addRow("Complemento", self.addresscomplemento)

        self.addresscidade = QLineEdit()
        self.addresscidade.setPlaceholderText("Cidade")
        form_layout.addRow("Cidade", self.addresscidade)

        self.cep = QLineEdit()
        self.cep.setPlaceholderText("CEP")
        form_layout.addRow("CEP", self.cep)

        self.ederecoNumero = QLineEdit()
        self.ederecoNumero.setPlaceholderText("Nr.")
        form_layout.addRow("Nr.:", self.ederecoNumero)

        layout.addStretch(1)
        layout.addLayout(form_layout)
        self.GroupBox4.setLayout(layout)

    def createGroupBoxSalvar(self):
        self.GroupBox3 = QGroupBox("Salvar Cadastro")

        self.defaultPushButton = QPushButton("Salvar")
        self.defaultPushButton.setDefault(True)
        self.defaultPushButton.clicked.connect(self.addcliente)

        self.defaultPushButton2 = QPushButton(self)
        self.defaultPushButton2.setDefault(True)
        self.defaultPushButton2.setIcon(QIcon("Icones/sair.png"))
        self.defaultPushButton2.setIconSize(QSize(20, 20))
        self.defaultPushButton2.setMinimumHeight(25)
        self.defaultPushButton2.clicked.connect(self.closeCadastro)

        layout = QGridLayout()
        layout.addWidget(self.defaultPushButton, 1, 0, 1, 2)
        layout.addWidget(self.defaultPushButton2, 2, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.GroupBox3.setLayout(layout)

    def addcliente(self):
        tipo = self.branchinput.itemText(self.branchinput.currentIndex())
        nome = self.nameinput.text()
        cpf = self.cpfinput.text()
        rg = self.rginput.text()
        tel = self.mobileinput.text()
        endereco = self.addressinput.text()
        bairro = self.bairro.text()
        complemento = self.addresscomplemento.text()
        numero = self.ederecoNumero.text()
        cep = self.cep.text()
        cidade = self.addresscidade.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = "INSERT INTO clientes (tipo, nome, cpf, rg, telefone, endereco, complemento, bairro, numero, cep, cidade) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dados = (
                tipo,
                nome,
                cpf,
                rg,
                tel,
                endereco,
                complemento,
                bairro,
                numero,
                cep,
                cidade,
            )
            self.cursor.execute(comando_sql, dados)

            conexao.banco.commit()
            self.cursor.close()

            # limpa os campos
            self.nameinput.setText("")
            self.cpfinput.setText("")
            self.rginput.setText("")
            self.mobileinput.setText("")
            self.addressinput.setText("")
            self.addressinput.setText("")
            self.bairro.setText("")
            self.addresscomplemento.setText("")
            self.ederecoNumero.setText("")
            self.cep.setText("")
            self.addresscidade.setText("")
            self.bairro.setText("")
            self.addresscomplemento.setText("")
            self.ederecoNumero.setText("")
            self.cep.setText("")
            self.addresscidade.setText("")

        except Exception:
            QMessageBox.warning(
                QMessageBox(), "aleleonel@gmail.com", "A inserção falhou!"
            )

    def closeCadastro(self):
        self.close()


class DeleteClientes(QDialog):
    """
    Define uma nova janela onde executaremos
    a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteClientes, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        self.setWindowTitle("Deletar Cliente")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de deletar
        self.QBtn.clicked.connect(self.deletecliente)

        layout = QVBoxLayout()

        # Cria as caixas de digitação e
        # verifica se é um numero
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Codigo do cliente - somente número")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletecliente(self):
        delroll = ""
        delroll = self.deleteinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql = "DELETE FROM clientes WHERE codigo = " + str(delroll)
            self.cursor.execute(consulta_sql)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(
                QMessageBox(), "Deleção realizada com sucesso!", "DELETADO COM SUCESSO!"
            )
            self.close()

        except Exception:
            QMessageBox.warning(
                QMessageBox(), "aleleonel@gmail.com", "A Deleção falhou!"
            )


class CadastroProdutos(QDialog):
    def __init__(self, parent=None):
        super(CadastroProdutos, self).__init__(parent)

        self.createTopLeftGroupBox()
        self.createGroupBoxSalvar()
        self.createGroupBox()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

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

    def createTopLeftGroupBox(self):
        self.GroupBox1 = QGroupBox("Cadastro de Itens")

        # Insere o ramo ou tipo  /
        # Criar uma tabela para cadastrar unidade de medida
        self.uninput = QComboBox()
        self.uninput.addItem("UN")
        self.uninput.addItem("PÇ")
        self.uninput.addItem("KG")
        self.uninput.addItem("LT")
        self.uninput.addItem("PT")
        self.uninput.addItem("CX")

        self.codigo_produto = QLabel("Codigo")
        self.cdprod = QLineEdit()
        self.codigo_produto.setAlignment(Qt.AlignLeft)

        self.codigo_ean = QLabel("EAN")
        self.eanprod = QLineEdit()
        self.codigo_ean.setAlignment(Qt.AlignCenter)

        self.codigo_gtin = QLabel("GTIN")
        self.gtinprod = QLineEdit()
        self.codigo_gtin.setAlignment(Qt.AlignRight)

        layout = QHBoxLayout()
        layout.addWidget(self.codigo_produto)
        layout.addWidget(self.cdprod)

        layout.addWidget(self.codigo_ean)
        layout.addWidget(self.eanprod)

        layout.addWidget(self.codigo_gtin)
        layout.addWidget(self.gtinprod)

        layout.addWidget(self.uninput)

        layout.addStretch(1)
        self.GroupBox1.setLayout(layout)

    def createGroupBox(self):
        self.GroupBox2 = QGroupBox()

        self.label_descricao = QLabel("Descrição", self)
        self.label_descricao.setAlignment(Qt.AlignLeft)
        self.descricao = QLineEdit()
        self.descricao.setFixedSize(447, 25)

        self.label_custo = QLabel("Preço de Custo", self)
        self.label_custo.setAlignment(Qt.AlignLeft)
        self.precocusto = QLineEdit()
        self.precocusto.setFixedSize(107, 25)

        self.label_venda = QLabel("Preço de Venda", self)
        self.label_venda.setAlignment(Qt.AlignLeft)
        self.preco = QLineEdit()
        self.preco.setFixedSize(107, 25)

        layout = QVBoxLayout()

        layout.addWidget(self.label_descricao)
        layout.addWidget(self.descricao)

        layout.addWidget(self.label_custo)
        layout.addWidget(self.precocusto)

        layout.addWidget(self.label_venda)
        layout.addWidget(self.preco)

        layout.addStretch(1)
        self.GroupBox2.setLayout(layout)

    def createGroupBoxSalvar(self):
        self.GroupBox3 = QGroupBox("Salvar Cadastro")

        self.defaultPushButton = QPushButton("Salvar")
        self.defaultPushButton.setDefault(True)
        self.defaultPushButton.clicked.connect(self.addproduto)

        self.defaultPushButton2 = QPushButton("Fechar")
        self.defaultPushButton2.setDefault(True)
        self.defaultPushButton2.clicked.connect(self.closeCadastro)

        layout = QGridLayout()
        layout.addWidget(self.defaultPushButton, 1, 0, 1, 2)
        layout.addWidget(self.defaultPushButton2, 2, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.GroupBox3.setLayout(layout)

    def addproduto(self):
        """
        captura as informações digitadas
        no lineedit e armazena nas variaveis
        :return:
        """
        descricao = self.descricao.text()
        ncm = self.eanprod.text()
        un = self.uninput.itemText(self.uninput.currentIndex())
        preco = self.preco.text()

        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = (
                "INSERT INTO produtos (descricao, ncm, un, preco)"
                "VALUES (%s,%s,%s,%s)"
            )
            dados = descricao, ncm, un, str(preco)
            self.cursor.execute(comando_sql, dados)
            conexao.banco.commit()
            self.cursor.close()

            self.cdprod.setText("")
            self.descricao.setText("")
            self.eanprod.setText("")
            # self.uninput.itemText(self.uninput.currentIndex())
            self.precocusto.setText("")
            self.preco.setText("")

        except Exception:
            QMessageBox.warning(
                QMessageBox(), "aleleonel@gmail.com", "A inserção falhou!"
            )

    def closeCadastro(self):
        self.close()


class ListProdutos(QMainWindow):
    def __init__(self):
        super(ListProdutos, self).__init__()
        self.setWindowIcon(QIcon("Icones/produtos2.png"))

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PRODUTOS")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(5)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Codigo",
                "Descrição",
                "NCM",
                "UN",
                "Preço Venda",
            )
        )

        self.cursor = conexao.banco.cursor()
        comando_sql = """
                        SELECT a.codigo, a.descricao, a.ncm, a.un, a.preco
                        FROM controle_clientes.produtos as a
                        """

        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("Icones/add.png"), "Add Produto", self)
        btn_ac_adduser.triggered.connect(self.cadProdutos)
        btn_ac_adduser.setStatusTip("Add Produto")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(
            QIcon("Icones/atualizar.png"), "Atualizar dados do produto", self
        )
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_delete = QAction(QIcon("Icones/deletar.png"), "Deletar o Produto", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        btn_ac_search = QAction(
            QIcon("Icones/pesquisa.png"), "Pesquisar dados por produto", self
        )
        btn_ac_search.triggered.connect(self.searchProduto)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_sair = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_sair.triggered.connect(self.fechar)
        toolbar.addAction(btn_ac_sair)

        self.show()

    def loaddata(self):
        self.cursor = conexao.banco.cursor()
        comando_sql = """
                                SELECT a.codigo, a.descricao, a.ncm, a.un, a.preco
                                FROM controle_clientes.produtos as a ;
                                """
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(5)

        for i in range(0, len(result)):
            for j in range(0, 5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadProdutos(self):
        dlg = CadastroProdutos()
        dlg.exec()
        self.loaddata()

    def searchProduto(self):
        dlg = SearchProdutos()
        dlg.exec_()

    def delete(self):
        dlg = DeleteProduto()
        dlg.exec_()
        self.loaddata()

    def fechar(self):
        self.close()


class SearchProdutos(QDialog, ConsultaProdutosEstoque):
    def __init__(self, parent=None):
        super(SearchProdutos, self).__init__(parent)

        self.editDialog = None  # Variável para armazenar o EditDialog

        self.createTopLeftGroupBox()
        self.createGroupBoxSalvar()
        self.createGroupBox()
        self.buscaregistrosProdutos()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

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

        self.setWindowTitle("CONSULTA DE PRODUTOS")

    def createTopLeftGroupBox(self):
        self.GroupBox1 = QGroupBox("Cadastro de Itens")

        # Insere o ramo ou tipo  /
        # Criar uma tabela para cadastrar unidade de medida
        self.uninput = QLineEdit()
        self.uninput.setFixedSize(35, 25)

        self.codigo_produto = QLabel("Codigo")
        self.cdprod = QLineEdit()
        self.cdprod.returnPressed.connect(self.setFocusAndCallFunction2)
        self.codigo_produto.setAlignment(Qt.AlignLeft)
        self.cdprod.setFixedSize(60, 25)

        self.codigo_ean = QLabel("EAN")
        self.eanprod = QLineEdit()
        self.codigo_ean.setAlignment(Qt.AlignCenter)
        self.eanprod.setFixedSize(100, 25)

        self.codigo_gtin = QLabel("GTIN")
        self.gtinprod = QLineEdit()
        self.codigo_gtin.setAlignment(Qt.AlignRight)
        self.gtinprod.setFixedSize(200, 25)

        # Adicione uma instância do modelo de dados
        self.headers = [
            "codigo",
            "Desricao",
            "Preco",
            "NCM",
            "UN",
            "STATUS",
        ]
        self.model = ProdutoTableModel([], self.headers)
        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        layout = QHBoxLayout()

        layout.addWidget(self.codigo_produto)
        layout.addWidget(self.cdprod)

        layout.addWidget(self.codigo_ean)
        layout.addWidget(self.eanprod)

        layout.addWidget(self.codigo_gtin)
        layout.addWidget(self.gtinprod)

        layout.addWidget(self.uninput)

        layout.addStretch(1)
        self.GroupBox1.setLayout(layout)

    def createGroupBox(self):
        # vai buscar na Classe ConsultaProdutosEstoque
        produtos = self.consultar_produtos_geral()

        self.GroupBox2 = QGroupBox()

        self.checkbox = QCheckBox("Ativo")
        self.checkbox.setChecked(True)  # Inicialmente definido como ativo
        self.checkbox.setFixedSize(100, 25)

        self.label_descricao = QLabel("Descrição", self)
        self.label_descricao.setAlignment(Qt.AlignLeft)

        self.descricao = QLineEdit()
        self.descricao.setPlaceholderText("Descrição / Produto")
        self.descricao.setFocus(True)

        # Configuração do autocompletar
        self.model_prod = QStandardItemModel()
        for produto in produtos:
            item = QStandardItem(produto)
            self.model_prod.appendRow(item)

        completer_prod = QCompleter(self.model_prod, self)
        completer_prod.setCaseSensitivity(Qt.CaseInsensitive)
        self.descricao.setCompleter(completer_prod)
        # self.descricao.returnPressed.connect(self.consultaProdutolist)
        self.descricao.returnPressed.connect(self.setFocusAndCallFunction)

        self.descricao.setFixedSize(447, 25)

        self.label_custo = QLabel("Preço de Custo", self)
        self.label_custo.setAlignment(Qt.AlignLeft)
        self.precocusto = QLineEdit()
        self.precocusto.setFixedSize(107, 25)

        self.label_venda = QLabel("Preço de Venda", self)
        self.label_venda.setAlignment(Qt.AlignLeft)
        self.preco = QLineEdit()
        self.preco.setFixedSize(107, 25)

        layout = QVBoxLayout()

        layout.addWidget(self.checkbox)

        layout.addWidget(self.label_descricao)
        layout.addWidget(self.descricao)

        layout.addWidget(self.label_custo)
        layout.addWidget(self.precocusto)

        layout.addWidget(self.label_venda)
        layout.addWidget(self.preco)

        layout.addStretch(1)
        self.GroupBox2.setLayout(layout)

        # Conecta o slot para atualizar o banco de dados quando o checkbox for alterado
        self.checkbox.stateChanged.connect(self.alterarProdutosStatus)

    def setFocusAndCallFunction(self):
        self.precocusto.setFocus()
        self.consultaProdutolist()

    def setFocusAndCallFunction2(self):
        self.precocusto.setFocus()
        if self.editButton.hasFocus():
            self.editButton.clearFocus()
        self.consultaCodigolist()

    def createGroupBoxSalvar(self):
        self.GroupBox3 = QGroupBox()

        # Adicione botões para avançar e voltar
        self.firstButton = QPushButton("Primeiro")
        self.nextButton = QPushButton("Próximo")
        self.prevButton = QPushButton("Anterior")
        self.lastButton = QPushButton("Último")

        self.nextButton.clicked.connect(self.avancarRegistro)
        self.prevButton.clicked.connect(self.voltarRegistro)
        self.firstButton.clicked.connect(self.voltarPrimeiroRegistro)
        self.lastButton.clicked.connect(self.avancarUltimoRegistro)

        self.editButton = QPushButton("Editar")
        self.editButton.clicked.connect(self.editarRegistro)

        self.defaultPushButton2 = QPushButton("Fechar")
        self.defaultPushButton2.setDefault(False)
        self.defaultPushButton2.setAutoDefault(False)
        self.defaultPushButton2.clearFocus()
        self.defaultPushButton2.clicked.connect(self.closeConsulta)

        layout = QGridLayout()

        # Modifique a disposição dos botões
        layout.addWidget(self.editButton, 1, 0)
        layout.addWidget(self.firstButton, 2, 0)
        layout.addWidget(self.prevButton, 2, 1)
        layout.addWidget(self.nextButton, 2, 2)
        layout.addWidget(self.lastButton, 2, 3)
        layout.addWidget(self.defaultPushButton2, 1, 1)
        layout.setRowStretch(5, 1)
        self.GroupBox3.setLayout(layout)

        # Inicializa a variável para rastrear o índice do registro atual
        self.current_record_index = 0
        self.records = []

    def buscaregistrosProdutos(self):
        try:
            self.cursor = conexao.banco.cursor()
            comando_sql = """SELECT p.codigo, p.descricao, p.preco, p.ncm, p.un, p.status, MAX(e.preco_compra) as preco_compra
                            FROM produtos as p
                            INNER JOIN controle_clientes.estoque as e
                            ON e.idproduto = p.codigo
                            WHERE e.status = '{}'
                            AND e.estoque > '{}'
                            GROUP BY p.codigo, p.descricao, p.preco, p.ncm, p.un""".format(
                "E", 0
            )

            self.cursor.execute(comando_sql)
            result = self.cursor.fetchall()
            self.cursor.close()

            # Atualiza o modelo de dados com os registros obtidos
            self.records = [item for item in result if item]
            self.model = ProdutoTableModel(self.records, self.headers)
            self.tableView.setModel(self.model)
            self.current_record_index = 0

            if not self.records:
                QMessageBox.information(
                    self, "Informação", "Nenhum registro encontrado para a pesquisa."
                )

            # Atualize os campos com base no registro atual
            self.atualizarCampos()

            # Atualize a habilitação dos botões de navegação
            self.updateNavigationButtons()

        except Exception as e:
            QMessageBox.warning(
                QMessageBox(), "Erro", f"A busca de registros falhou: {str(e)}"
            )

    def alterarProdutosStatus(self):
        if 0 <= self.current_record_index < len(self.records):
            cursor = conexao.banco.cursor()

            novo_status = (
                1 if self.checkbox.isChecked() else 0
            )  # 1 para ativo, 0 para inativo

            query = (
                "UPDATE controle_clientes.produtos SET status = %s WHERE codigo = %s"
            )
            id_registro = self.records[self.current_record_index][
                0
            ]  # Obtém o ID do registro atual

            cursor.execute(query, (novo_status, id_registro))
            conexao.banco.commit()

    def avancarRegistro(self):
        if self.current_record_index < len(self.records) - 1:
            self.current_record_index += 1
            self.atualizarCampos()
            self.updateNavigationButtons()

    def voltarRegistro(self):
        if self.current_record_index > 0:
            self.current_record_index -= 1
            self.atualizarCampos()
            self.updateNavigationButtons()

    def avancarUltimoRegistro(self):
        if len(self.records) > 0:
            self.current_record_index = len(self.records) - 1
            self.atualizarCampos()
            self.updateNavigationButtons()

    def voltarPrimeiroRegistro(self):
        if len(self.records) > 0:
            self.current_record_index = 0
            self.atualizarCampos()
            self.updateNavigationButtons()

    def atualizarCampos(self):
        if 0 <= self.current_record_index < len(self.records):
            # Atualizar os campos com base no registro atual
            record = self.records[self.current_record_index]

            self.cdprod.setText(str(record[0]))
            self.descricao.setText(str(record[1]))
            self.preco.setText(str(record[2]))
            self.eanprod.setText(str(record[3]))
            self.uninput.setText(str(record[4]))
            self.precocusto.setText(str(record[6]))

            # Atualiza o status do checkbox com base no registro atual
            self.checkbox.setChecked(bool(record[5]))

            # implementar codigo GTIN
            self.gtinprod.setText("")

    def updateNavigationButtons(self):
        num_records = len(self.records)
        if num_records == 0:
            self.firstButton.setEnabled(False)
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(False)
            self.lastButton.setEnabled(False)
        elif self.current_record_index == 0:
            self.firstButton.setEnabled(False)
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
            self.lastButton.setEnabled(True)
        elif self.current_record_index == num_records - 1:
            self.firstButton.setEnabled(True)
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
            self.lastButton.setEnabled(False)
        else:
            self.firstButton.setEnabled(True)
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)
            self.lastButton.setEnabled(True)

    def consultaProdutolist(self):
        self.consulta = self.descricao.text().upper()

        try:
            result = self.consultaProdutosLista(self.consulta)

            self.cdprod.setText(str(result[0][0]))
            self.descricao.setText(str(result[0][1]))
            self.preco.setText(str(result[0][2]))
            self.eanprod.setText(str(result[0][3]))
            self.uninput.setText(str(result[0][4]))
            self.precocusto.setText(str(result[0][5]))
            self.gtinprod.setText("")

        except Exception as e:
            QMessageBox.warning(
                self,
                "Erro",
                str(e),
            )

        # Armazena os registros e define o índice atual para 0
        self.records = [item for item in result if item]
        self.current_record_index = 0

        # Atualize os campos com base no registro atual
        self.atualizarCampos()

    def consultaCodigolist(self):
        self.consultacodigo = self.cdprod.text()

        try:
            result = self.consultaCodigoslista(self.consultacodigo)

            if not result:
                # Se nenhum resultado for encontrado, exiba uma mensagem
                QMessageBox.information(
                    self,
                    "Informação",
                    "Nenhum registro encontrado para o código fornecido.",
                )
                return

            self.cdprod.setText(str(result[0][0]))
            self.descricao.setText(str(result[0][1]))
            self.eanprod.setText(str(result[0][2]))
            self.uninput.setCurrentText(str(result[0][3]))
            self.preco.setText(str(result[0][4]))
            self.precocusto.setText(str(result[0][5]))
            self.gtinprod.setText("")

            # Armazene os registros e defina o índice atual para 0
            self.records = [item for item in result if item]
            self.current_record_index = 0

            # Atualize os campos com base no registro atual
            self.atualizarCampos()

        except Exception as e:
            QMessageBox.warning(self, "Erro", str(e))

    def editarRegistro(self):
        if self.current_record_index < len(self.records):
            # Obtenha o registro atual
            record = self.records[self.current_record_index]

            # Abra uma janela de edição de registro ou um diálogo de edição aqui
            # Passe os dados do registro para a janela de edição

            # Por exemplo, você pode criar uma nova janela de edição:
            editDialog = EditProdutosDialog(record)

            # Conecte um sinal para atualizar os dados após a edição ser concluída
            editDialog.edicaoConcluida.connect(self.atualizarRegistroEditado)

            # Exiba a janela de edição
            editDialog.exec_()

    def atualizarRegistroEditado(self):
        self.close()

    def closeConsulta(self):
        self.hide()


class DeleteProduto(QDialog):
    """
    Define uma nova janela onde executaremos
    a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteProduto, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        self.setWindowTitle("Deletar Produto")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de deletar
        self.QBtn.clicked.connect(self.deleteproduto)

        layout = QVBoxLayout()

        # Cria as caixas de digitação e
        # verifica se é um numero
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Codigo do produto - somente número")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteproduto(self):
        delroll = ""
        delroll = self.deleteinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql = "DELETE FROM produtos WHERE codigo = " + str(delroll)
            self.cursor.execute(consulta_sql)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(
                QMessageBox(),
                "Deleção realizada com sucesso!",
                "PRODUTO DELETADO COM SUCESSO!",
            )
            self.close()

        except Exception:
            QMessageBox.warning(
                QMessageBox(), "aleleonel@gmail.com", "A Deleção falhou!"
            )


class ListClientes(QMainWindow):
    def __init__(self):
        super(ListClientes, self).__init__()

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE CLIENTES")
        self.setMinimumSize(800, 600)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(13)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Codigo",
                "Tipo",
                "Nome",
                "CPF",
                "RG",
                "Telefone",
                "Endereco",
                "Complemento",
                "Bairro",
                "Número",
                "CEP",
                "Cidade",
                "Data",
            )
        )

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM clientes"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(13)

        for i in range(0, len(result)):
            for j in range(0, 13):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # botões do menu
        btn_ac_adduser = QAction(QIcon("Icones/add.png"), "Cadastro de Cliente", self)
        btn_ac_adduser.triggered.connect(self.cadClientes)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresch = QAction(
            QIcon("Icones/atualizar.png"), "Atualizar dados do Cliente", self
        )
        btn_ac_refresch.triggered.connect(self.loaddata)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        btn_ac_search = QAction(
            QIcon("Icones/pesquisa.png"), "Pesquisar dados por Cliente", self
        )
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Pesquisar")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("Icones/deletar.png"), "Deletar o Cliente", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Deletar ")
        toolbar.addAction(btn_ac_delete)

        btn_ac_sair = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_sair.triggered.connect(self.fechar)
        btn_ac_sair.setStatusTip("Sair ")
        toolbar.addAction(btn_ac_sair)

        self.show()

    def loaddata(self):
        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM clientes"
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)

        for i in range(0, len(result)):
            for j in range(0, 7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def cadClientes(self):
        dlg = CadastroClientes()
        dlg.exec()
        self.loaddata()

    def search(self):
        dlg = SearchClientes()
        dlg.exec_()

    def delete(self):
        dlg = DeleteCliente()
        dlg.exec_()
        self.loaddata()

    def fechar(self):
        self.close()


class DeleteCliente(QDialog):
    """
    Define uma nova janela onde executaremos
    a busca no banco
    """

    def __init__(self, *args, **kwargs):
        super(DeleteCliente, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Deletar")

        self.setWindowTitle("Deletar Cliente")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Chama a função de deletar
        self.QBtn.clicked.connect(self.deletecliente)

        layout = QVBoxLayout()

        # Cria as caixas de digitação e
        # verifica se é um numero
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Codigo do cliente - somente número")
        layout.addWidget(self.deleteinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletecliente(self):
        delroll = ""
        delroll = self.deleteinput.text()

        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql = "DELETE FROM clientes WHERE codigo = " + str(delroll)
            self.cursor.execute(consulta_sql)

            conexao.banco.commit()
            self.cursor.close()

            QMessageBox.information(
                QMessageBox(), "Deleção realizada com sucesso!", "DELETADO COM SUCESSO!"
            )
            self.close()

        except Exception:
            QMessageBox.warning(
                QMessageBox(), "aleleonel@gmail.com", "A Deleção falhou!"
            )


class DecimalLineEdit(QLineEdit):
    """Classe que define um QlineEdit como numérico"""

    def __init__(self):
        super().__init__()

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Comma or event.key() == Qt.Key_Period:
                # Substituir vírgula por ponto
                self.insert("0.")
                return True
            elif event.text().isdigit() or (
                event.text() == "-" and self.cursorPosition() == 0
            ):
                # Apenas números ou sinal negativo no início são permitidos
                return super().eventFilter(obj, event)
            else:
                return True  # Ignorar outros caracteres

        return super().eventFilter(obj, event)


class AberturaCaixa(QDialog):
    """
    Define uma nova janela onde inserimos os valores de abertura do caixa do dia
    """

    # Remover o botão fechar

    def __init__(self, *args, **kwargs):
        super(AberturaCaixa, self).__init__(*args, **kwargs)

        self.d = QDate.currentDate()
        self.dataAtual = self.d.toString(Qt.ISODate)
        self.dataAtual = str(self.dataAtual)

        layout = QVBoxLayout()

        self.setWindowTitle("Abertura do Caixa :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.lbl_titulo = QLabel("Caixa")
        self.lbl_titulo.setFont(QFont("Times", 42, QFont.Bold))
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_titulo)

        self.dataabertura = QLineEdit()
        self.dataabertura.setPlaceholderText(self.dataAtual)
        self.dataabertura.setEnabled(False)
        layout.addWidget(self.dataabertura)

        self.caixainicio = DecimalLineEdit()
        self.onlyFloat = QDoubleValidator()
        self.onlyFloat.setNotation(QDoubleValidator.StandardNotation)
        self.caixainicio.setValidator(self.onlyFloat)
        self.caixainicio.setPlaceholderText("R$ Valor inicial")
        layout.addWidget(self.caixainicio)
        self.caixainicio.textChanged[str].connect(self.check_disable)

        self.buttonAdd = QPushButton("Add.", self)
        self.buttonAdd.setIcon(QIcon("Icones/add.png"))
        self.buttonAdd.setIconSize(QSize(40, 40))
        self.buttonAdd.setMinimumHeight(40)
        self.buttonAdd.setEnabled(False)
        self.buttonAdd.clicked.connect(self.livrocaixa)
        layout.addWidget(self.buttonAdd)
        self.setLayout(layout)

        # self.caixainicio.textChanged[str].connect(self.check_disable)

        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()  # Ignorar a tecla ESC para evitar fechar o diálogo

    def check_disable(self):
        """Habilita o botão adicionar valor livro caixa apenas se tiver valor no text"""
        if self.caixainicio.text():
            self.buttonAdd.setEnabled(True)

        else:
            self.buttonAdd.setEnabled(False)

    def livrocaixa(self):
        self.d = QDate.currentDate()
        self.dataAtual = self.d.toString(Qt.ISODate)
        self.dataAtual = str(self.dataAtual)
        self.status = "I"
        self.valorcaixainiado = 0
        self.valorfechamento = 0
        self.total = 0

        # Defina o local para o Brasil
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

        if self.caixainicio.text() == ",":
            self.caixainicio.setText("0,00")

        self.valorcaixainiado += float(self.caixainicio.text().replace(",", "."))
        self.total += self.valorcaixainiado + self.valorfechamento

        self.cursor = conexao.banco.cursor()
        comando_sql = "INSERT INTO livro (dataAtual, valor, valorfechamento,total, status) VALUES (%s, %s, %s, %s,%s)"
        dados = (
            self.dataAtual,
            self.valorcaixainiado,
            self.valorfechamento,
            self.total,
            self.status,
        )
        self.cursor.execute(comando_sql, dados)
        conexao.banco.commit()
        # self.close()

        self.hide()


class FechamentoCaixa(QDialog):
    """
    Define uma nova janela onde inserimos os valores de abertura do caixa do dia
    """

    def __init__(self, *args, **kwargs):
        super(FechamentoCaixa, self).__init__(*args, **kwargs)

        self.d = QDate.currentDate()
        self.dataAtual = self.d.toString(Qt.ISODate)
        self.dataAtual = str(self.dataAtual)

        layout = QVBoxLayout()

        self.setWindowTitle("Fechamento do Caixa :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.lbl_titulo = QLabel("Caixa")
        self.lbl_titulo.setFont(QFont("Times", 42, QFont.Bold))
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_titulo)

        self.datafechamento = QLineEdit()
        self.datafechamento.setPlaceholderText(self.dataAtual)
        self.datafechamento.setEnabled(False)
        layout.addWidget(self.datafechamento)

        self.caixafechamento = DecimalLineEdit()
        self.onlyFloat = QDoubleValidator()
        self.caixafechamento.setValidator(self.onlyFloat)
        self.caixafechamento.setPlaceholderText("R$ Valor fechamento")
        layout.addWidget(self.caixafechamento)

        self.buttonAdd = QPushButton("Add.", self)
        self.buttonAdd.setIcon(QIcon("Icones/add.png"))
        self.buttonAdd.setIconSize(QSize(40, 40))
        self.buttonAdd.setMinimumHeight(40)
        self.buttonAdd.setEnabled(False)
        self.buttonAdd.clicked.connect(self.livrocaixa)
        layout.addWidget(self.buttonAdd)
        self.setLayout(layout)

        # remove o botão fechar do Qdialog
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.caixafechamento.textChanged[str].connect(self.check_disable)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()  # Ignorar a tecla ESC para evitar fechar o diálogo

    def check_disable(self):
        """Habilita o botão adicionar valor livro caixa apenas se tiver valor no text"""
        if self.caixafechamento.text():
            self.buttonAdd.setEnabled(True)

        else:
            self.buttonAdd.setEnabled(False)

    def livrocaixa(self):
        try:
            # varrer a tabela livro para pegar o valorcaixainiciado
            self.cursor = conexao.banco.cursor()
            consulta_sql = "SELECT status FROM livro ORDER BY idlivro DESC limit 1;"
            self.cursor.execute(consulta_sql)
            self.status_final = self.cursor.fetchall()

            self.status_finalizado = [resultado for resultado in self.status_final]
            print(
                "Mostra a ultima linha do status do fechamento", self.status_finalizado
            )
        except:
            print("erro ao conectar")

        self.d = QDate.currentDate()
        self.dataAtual = self.d.toString(Qt.ISODate)
        self.dataAtual = str(self.dataAtual)
        self.status = "F"
        self.valorcaixainiado = (
            0  # precisa pegar da tabela, esse valor ja exite na tabela
        )
        # esse valor será inserido no momento do fechamento (digitado)
        self.valorfechamento = 0
        self.total = 0

        if self.caixafechamento.text() == ",":
            self.caixafechamento.setText("0,00")

        self.valorfechamento += float(self.caixafechamento.text().replace(",", "."))

        # varrer a tabela livro para pegar o valorcaixainiciado
        self.cursor = conexao.banco.cursor()
        consulta_sql = (
            "SELECT * FROM livro WHERE status = 'I' ORDER BY idlivro DESC limit 1;"
        )
        self.cursor.execute(consulta_sql)
        self.result = self.cursor.fetchall()

        self.fecha_indice = [resultado for resultado in self.result]

        for indice in range(len(self.fecha_indice)):
            # precisa pegar da tabela, esse valor ja exite na tabela
            self.valorcaixainiado = self.fecha_indice[indice][2]

        self.total += (
            self.valorcaixainiado + self.valorfechamento
        ) - self.valorcaixainiado

        # inserir a somatória valor de entrada e valor do fechamento
        self.cursor = conexao.banco.cursor()
        comando_sql = "INSERT INTO livro (dataAtual, valor, valorfechamento,total, status) VALUES (%s, %s, %s, %s,%s)"
        dados = (
            self.dataAtual,
            self.valorcaixainiado,
            self.valorfechamento,
            self.total,
            self.status,
        )
        self.cursor.execute(comando_sql, dados)
        conexao.banco.commit()
        # self.close()

        self.hide()


class DataEntryForm(QWidget, ConsultaProdutosEstoque):
    def __init__(self):
        super().__init__()

        self.consulta_clientes()  # consulta banco de dados cadastro de clientes

        self.preco = 0
        self.TOTAL = 0

        self.items = 0
        self.total = list()
        self.calculaitens = list()
        self._data = {}

        d = QDate.currentDate()
        dataAtual = d.toString(Qt.ISODate)
        data_pedido = str(dataAtual)

        # left side
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        #                                       0         1          2        3            4
        self.table.setHorizontalHeaderLabels(
            ("Cod.", "Descrição", "Qtd", "Preço Un.", "Sub Total")
        )
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.ResizeToContents
        )

        self.layoutRight = QVBoxLayout()

        self.layoutRight.setSpacing(10)

        self.butonAbrirCaixa = QPushButton("Abrir Caixa", self)
        self.butonAbrirCaixa.setIcon(QIcon("Icones/dollars.png"))
        self.butonAbrirCaixa.setIconSize(QSize(40, 40))
        self.butonAbrirCaixa.setMinimumHeight(40)
        self.layoutRight.addWidget(self.butonAbrirCaixa)

        self.butonFecharCaixa = QPushButton("Fechar Caixa", self)
        self.butonFecharCaixa.setIcon(QIcon("Icones/quit.png"))
        self.butonFecharCaixa.setIconSize(QSize(40, 40))
        self.butonFecharCaixa.setMinimumHeight(40)
        # self.butonFecharCaixa.setEnabled(False)
        self.layoutRight.addWidget(self.butonFecharCaixa)

        self.lbl_titulo = QLabel("Caixa")
        self.lbl_titulo.setFont(QFont("Times", 42, QFont.Bold))
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.layoutRight.addWidget(self.lbl_titulo)

        self.lineEditdata = QLineEdit()
        self.lineEditdata.setText(data_pedido)
        self.lineEditdata.setEnabled(False)
        self.layoutRight.addWidget(self.lineEditdata)

        self.lineEditCliente = QLineEdit()
        self.lineEditCliente.setPlaceholderText("Nome / Razão")
        self.model = QStandardItemModel()
        self.model = self.clientes
        completer = QCompleter(self.model, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEditCliente.setCompleter(completer)
        self.lineEditCliente.editingFinished.connect(self.addCliente)
        self.lineEditCliente.setEnabled(False)

        self.layoutRight.addWidget(self.lineEditCliente)

        # vai buscar na Classe ConsultaProdutosEstoque
        produtos = self.consultar_produtos()

        self.lineEditDescription = QLineEdit()
        self.lineEditDescription.setPlaceholderText("Descrição / Produto")
        self.model_prod = QStandardItemModel()
        self.model_prod = produtos
        self.lineEditDescription.setEnabled(False)

        completer_prod = QCompleter(self.model_prod, self)
        completer_prod.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEditDescription.setCompleter(completer_prod)

        self.lineEditDescription.editingFinished.connect(self.addProdutos)
        self.layoutRight.addWidget(self.lineEditDescription)

        self.lineEditQtd = QLineEdit()
        self.onlyInt = QIntValidator()
        self.lineEditQtd.setValidator(self.onlyInt)
        self.lineEditQtd.setPlaceholderText("Quantidade")
        self.lineEditQtd.setEnabled(False)

        self.layoutRight.addWidget(self.lineEditQtd)

        self.lineEditPrice = QLineEdit()
        self.onlyFloat = QDoubleValidator()
        self.lineEditPrice.setValidator(self.onlyFloat)
        self.lineEditPrice.setPlaceholderText("R$: Preço")
        self.layoutRight.addWidget(self.lineEditPrice)
        self.lineEditPrice.setEnabled(False)

        self.lbl_total = QLabel()
        self.lbl_total.setText("R$ 0.00")
        self.lbl_total.setFont(QFont("Times", 42, QFont.Bold))
        self.lbl_total.setAlignment(Qt.AlignCenter)
        # self.lbl_total.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.layoutRight.addWidget(self.lbl_total)

        self.buttonAdd = QPushButton("Add.", self)
        self.buttonAdd.setIcon(QIcon("Icones/add.png"))
        self.buttonAdd.setIconSize(QSize(40, 40))
        self.buttonAdd.setMinimumHeight(40)
        self.buttonAdd.setEnabled(False)

        self.buttonClear = QPushButton("Canc.", self)
        self.buttonClear.setIcon(QIcon("Icones/clear.png"))
        self.buttonClear.setIconSize(QSize(40, 40))
        self.buttonClear.setMinimumHeight(40)
        # self.buttonClear.setEnabled(False)

        self.buttonClearOne = QPushButton("Rem.", self)
        self.buttonClearOne.setIcon(QIcon("Icones/clear.png"))
        self.buttonClearOne.setIconSize(QSize(40, 40))
        self.buttonClearOne.setMinimumHeight(40)
        # self.buttonClearOne.setEnabled(False)

        self.buttongerar = QPushButton("Gerar", self)
        self.buttongerar.setIcon(QIcon("Icones/dollars.png"))
        self.buttongerar.setIconSize(QSize(40, 40))
        self.buttongerar.setMinimumHeight(40)
        self.buttongerar.setEnabled(False)

        self.layoutRight.addWidget(self.buttonAdd)
        self.layoutRight.addWidget(self.buttongerar)
        self.layoutRight.addWidget(self.buttonClear)
        self.layoutRight.addWidget(self.buttonClearOne)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table, 0)
        self.layout.addLayout(self.layoutRight, 0)

        self.setLayout(self.layout)

        self.buttonClear.clicked.connect(self.reset_table)
        self.buttonClearOne.clicked.connect(self.excluir_dados)
        self.buttongerar.clicked.connect(self.gerar)
        self.buttonAdd.clicked.connect(self.add_entry)
        self.butonAbrirCaixa.clicked.connect(self.abrircaixa)
        self.butonFecharCaixa.clicked.connect(self.fecharcaixa)

        self.lineEditDescription.textChanged[str].connect(self.check_disable)
        self.lineEditPrice.textChanged[str].connect(self.check_disable)

        try:
            # varrer a tabela livro para pegar o valorcaixainiciado
            self.cursor = conexao.banco.cursor()
            consulta_sql = "SELECT status FROM livro ORDER BY idlivro DESC limit 1;"
            self.cursor.execute(consulta_sql)
            self.status_final = self.cursor.fetchall()

            self.status_finalizado = [resultado for resultado in self.status_final]

            for indice_final in range(len(self.status_finalizado)):
                self.status_finalizado[indice_final][0]

            aberto = self.status_finalizado[indice_final][0]
            if aberto == "I":
                self.butonAbrirCaixa.setEnabled(False)
                self.habilitaBotoesCaixa()

            else:
                # self.butonAbrirCaixa.setEnabled(True)
                self.butonFecharCaixa.setEnabled(False)

        except (RuntimeError, TypeError, NameError):
            pass

        self.fill_table()

    def consulta_clientes(self):
        self.cursor = conexao.banco.cursor()
        consulta_sql = "SELECT * FROM clientes where status = {} ".format(1)
        self.cursor.execute(consulta_sql)
        self.result = self.cursor.fetchall()

        self.clientes = []
        for i in range(len(self.result)):
            if self.result[i][2]:
                self.clientes.append(self.result[i][2])

        return self.result, self.clientes

    def habilitaBotoesCaixa(self):
        self.lineEditDescription.setEnabled(True)
        self.lineEditCliente.setEnabled(True)
        self.lineEditQtd.setEnabled(True)
        self.lineEditPrice.setEnabled(True)

    def abrircaixa(self):
        # self.butonAbrirCaixa.setEnabled(False)
        # self.butonFecharCaixa.setEnabled(True)
        try:
            # varrer a tabela livro para pegar o valorcaixainiciado
            self.cursor = conexao.banco.cursor()
            consulta_sql = "SELECT status FROM livro ORDER BY idlivro DESC limit 1;"
            self.cursor.execute(consulta_sql)
            self.status_final = self.cursor.fetchall()

            self.status_finalizado = [resultado for resultado in self.status_final]
            for indice_final in range(len(self.status_finalizado)):
                print(
                    "Mostra a ultima linha do status",
                    self.status_finalizado[indice_final][0],
                )
            aberto = self.status_finalizado[indice_final][0]
            if aberto != "I":
                replay = QMessageBox.question(
                    self,
                    "Window close",
                    "Deseja realmente Abrir o caixa?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )

            if replay == QMessageBox.Yes:
                self.butonAbrirCaixa.setEnabled(False)
                self.butonFecharCaixa.setEnabled(True)
                dlg = AberturaCaixa()
                dlg.exec()
                self.habilitaBotoesCaixa()
                self.closeEvent()

        except (RuntimeError, TypeError, NameError):
            print("RuntimeError", RuntimeError)
            print("TypeError", TypeError)
            print("NameError", NameError)

    def fecharcaixa(self, event):
        try:
            # varrer a tabela livro para pegar o valorcaixainiciado
            self.cursor = conexao.banco.cursor()
            consulta_sql = "SELECT status FROM livro ORDER BY idlivro DESC limit 1;"
            self.cursor.execute(consulta_sql)
            self.status_final = self.cursor.fetchall()

            self.status_finalizado = [resultado for resultado in self.status_final]
            for indice_final in range(len(self.status_finalizado)):
                print(
                    "Mostra a ultima linha do status",
                    self.status_finalizado[indice_final][0],
                )

            aberto = self.status_finalizado[indice_final][0]

            if aberto != "F":
                replay = QMessageBox.question(
                    self,
                    "Window close",
                    "Deseja realmente Fechar o caixa?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )

            if replay == QMessageBox.Yes:
                # dataAtual = QDate.currentDate()

                self.butonFecharCaixa.setEnabled(False)
                self.butonAbrirCaixa.setEnabled(True)

                self.soma_fechamento = 0
                valor_do_dia = []
                decimal_lista = []
                self.status = "F"
                self.desabilitaBotoesCaixa()
                dlg = FechamentoCaixa()
                dlg.exec()
            else:
                pass

        except (RuntimeError, TypeError, NameError):
            print("RuntimeError", str(RuntimeError))
            print("TypeError", str(TypeError))
            print("NameError", str(NameError))

    def desabilitaBotoesCaixa(self):
        self.lineEditDescription.setEnabled(False)
        self.lineEditCliente.setEnabled(False)
        self.lineEditQtd.setEnabled(False)
        self.lineEditPrice.setEnabled(False)

    def addCliente(self):
        entryItem = self.lineEditCliente.text()

    def addProdutos(self):
        self.cursor = conexao.banco.cursor()
        consulta_prod = "SELECT * FROM produtos"
        self.cursor.execute(consulta_prod)
        result_prod = self.cursor.fetchall()

        entryItem = self.lineEditDescription.text()

        for i in range(len(result_prod)):
            if result_prod[i][1] == entryItem:
                self.codigo = result_prod[i][0]
                self.preco = result_prod[i][2]
                print(type(self.preco))
                self.TOTAL += float(int(self.preco))
                self.lineEditPrice.setText(str(self.preco))

    def fill_table(self, data=None):
        data = self._data if not data else data

        for desc, price in data.items():
            descItem = QTableWidgetItem(desc)
            priceItem = QTableWidgetItem("${0:.2f}".format(price))
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, descItem)
            self.table.setItem(self.items, 1, priceItem)
            self.items += 1

    def add_entry(self):
        self.sub_total = 0
        self.buttongerar.setEnabled(True)
        if self.table.rowCount() > 0:
            self.calculaitens = []
            linha = self.table.rowCount()
            row = linha
            while row > 0:
                row -= 1
                col = self.table.columnCount()
                resultado = 0
                for x in range(0, col, 1):
                    self.headertext = self.table.horizontalHeaderItem(x).text()
                    if self.headertext == "Sub Total":
                        cabCol = x
                        resultado = self.table.item(row, cabCol).text()
                        recebe = resultado.replace("R$", "0")
                        self.calculaitens.append(float(recebe))

                self.ttotal = 0
                self.ttotal += sum(self.calculaitens)
                tot_format = "R${0:.2f} ".format(float(self.ttotal))
                self.lbl_total.setText(str(tot_format))

        self.cod = self.codigo
        self.desc = self.lineEditDescription.text()
        self.qtd = int(self.lineEditQtd.text())
        self.price = float(self.lineEditPrice.text())
        self.sub_total = float(self.qtd * self.price)
        self.sub_ttotal = str(self.sub_total)

        try:
            codItem = QTableWidgetItem(str(self.cod))
            descItem = QTableWidgetItem(self.desc)

            qtdItem = QTableWidgetItem(str(self.qtd))
            qtdItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            subItem = QTableWidgetItem("R${0:.2f} ".format(float(self.sub_ttotal)))
            subItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            priceItem = QTableWidgetItem("R${0:.2f} ".format(float(self.price)))
            priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, codItem)
            self.table.setItem(self.items, 1, descItem)
            self.table.setItem(self.items, 2, qtdItem)
            self.table.setItem(self.items, 3, priceItem)
            self.table.setItem(self.items, 4, subItem)

            # teste de calculo celula
            # dado um qtablewidget que tem uma linha selecionada ...
            # retorna o valor da coluna na mesma linha que corresponde a um determinado nome de coluna
            # fyi: o nome da coluna diferencia maiúsculas de minúsculas
            row = self.items
            col = self.table.columnCount()
            resultado = 0
            for x in range(0, col, 1):
                self.headertext = self.table.horizontalHeaderItem(x).text()
                if self.headertext == "Sub Total":
                    cabCol = x
                    resultado = self.table.item(row, cabCol).text()
                    recebe = resultado.replace("R$", "0")
                    self.calculaitens.append(float(recebe))
            self.items += 1
            self.ttotal = 0
            self.ttotal += sum(self.calculaitens)
            tot_format = "R${0:.2f} ".format(float(self.ttotal))
            self.lbl_total.setText(str(tot_format))

            self.lineEditDescription.setText("")
            self.lineEditQtd.setText("")
            self.lineEditPrice.setText("")
        except ValueError:
            pass

    def check_disable(self):
        if self.lineEditDescription.text() and self.lineEditPrice.text():
            self.lineEditQtd.setText("1")
            self.buttonAdd.setEnabled(True)
            self.buttongerar.setEnabled(False)
        else:
            self.buttonAdd.setEnabled(False)
            # self.buttongerar.setEnabled(False)

    # Botões de cancelameno de item e
    # cancelamento pedido
    def reset_table(self):
        self.table.setRowCount(0)
        self.items = 0
        self.ttotal = 0
        self.preco = 0
        self.TOTAL = 0
        # self.total = []
        self.calculaitens = []
        self.lineEditCliente.setText("")
        self.lineEditDescription.setText("")
        self.lineEditQtd.setText("")
        self.lineEditPrice.setText("")
        self.lbl_total.setText("R$ 0.00")
        self.buttongerar.setEnabled(False)

    # @QtCore.pyqtSlot()
    def excluir_dados(self):
        self.buttongerar.setEnabled(False)
        if self.table.rowCount() > 0:
            linha = self.table.currentRow()
            self.table.removeRow(linha)
            self.items -= 1
            self.lineEditDescription.setText("")
            self.lineEditQtd.setText("")
            self.lineEditPrice.setText("")

            self.calculaitens = []
            linha = self.table.rowCount()
            row = linha
            if row > 0:
                while row > 0:
                    self.buttongerar.setEnabled(True)
                    row -= 1
                    col = self.table.columnCount()
                    resultado = 0
                    for x in range(0, col, 1):
                        self.headertext = self.table.horizontalHeaderItem(x).text()
                        if self.headertext == "Sub Total":
                            cabCol = x
                            resultado = self.table.item(row, cabCol).text()
                            recebe = resultado.replace("R$", "0")
                            self.calculaitens.append(float(recebe))
                    self.ttotal = 0
                    self.ttotal += sum(self.calculaitens)
                    tot_format = "R${0:.2f} ".format(float(self.ttotal))
                    self.lbl_total.setText(str(tot_format))
            else:
                self.lbl_total.setText("R$ 0.00")
        else:
            self.lbl_total.setText("R$ 0.00")

    def numeroPedido(self):
        d = QDate.currentDate()
        data_anterior = str(d.addDays(-1).toString(Qt.ISODate))
        nr_caixa = 0

        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT * FROM pedidocaixa "
        self.cursor.execute(comando_sql)
        result_data = self.cursor.fetchall()
        for i in range(len(result_data)):
            # print(result_data[i][1])
            if nr_caixa == result_data[i][1]:
                nr_caixa += 1
            else:
                nr_caixa += 1
        return nr_caixa

    def codigoclientepedido(self):
        """Definir um codigo padrão para cliente balcão
        temporariamente devinido como 1. Pega o nome do
        cliente e o código correspondente"""

        self.cursor = conexao.banco.cursor()
        nome = self.lineEditCliente.text()
        comando_sql = "SELECT nome FROM clientes"
        self.cursor.execute(comando_sql)
        cli_nome = self.cursor.fetchall()
        nome_digitado = []
        for i in range(len(cli_nome)):
            print("selecionando o nome: ", cli_nome[i][0])
            nome_digitado.append(cli_nome[i][0])

        if nome == "" or nome not in nome_digitado:
            comando_sql = "SELECT codigo FROM clientes WHERE codigo ='{}' ".format(1)
            self.cursor.execute(comando_sql)
            cod_cli = self.cursor.fetchall()
            codigo = cod_cli[0][0]
        else:
            comando_sql = "SELECT codigo FROM clientes WHERE nome ='{}' ".format(nome)
            self.cursor.execute(comando_sql)
            cod_cli = self.cursor.fetchall()
            codigo = cod_cli[0][0]

        return codigo

    def gerar(self):
        d = QDate.currentDate()
        dataAtual = d.toString(Qt.ISODate)
        dataAtual = str(dataAtual)

        global fechamento
        fechamento = 0
        nr_caixa = self.numeroPedido()
        codigo = self.codigoclientepedido()

        self.cursor = conexao.banco.cursor()
        for i in range(self.table.rowCount()):
            self.cod_prod = self.table.item(i, 0).text()
            self.text = self.table.item(i, 1).text()
            self.qtd = float(self.table.item(i, 2).text())
            self.valUn = float(self.table.item(i, 3).text().replace("R$", ""))
            self.valTot = float(self.table.item(i, 4).text().replace("R$", ""))

            fechamento += self.valTot

            comando_sql = (
                "INSERT INTO pedidocaixa (nr_caixa, cod_produto, cod_vendedor, cod_cliente, quantidade,"
                "valor_total, ultupdate) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            )
            dados = nr_caixa, self.cod_prod, 1, codigo, self.qtd, self.valTot, dataAtual
            self.cursor.execute(comando_sql, dados)
            conexao.banco.commit()
        dlg = EfetivaPedidoCaixa(fechamento, nr_caixa)
        dlg.exec()
        return


class EfetivaPedidoCaixa(QDialog):
    def __init__(self, fechamento, nr_caixa):
        super(EfetivaPedidoCaixa, self).__init__()

        totaliza = "${0:.2f}".format(fechamento)
        n_caixa = nr_caixa
        # print("Parametro", n_caixa)

        # Configurações do titulo da Janela
        self.setWindowTitle("RECEBER R$:")
        self.setFixedWidth(600)
        self.setFixedHeight(600)

        layout = QVBoxLayout()
        self.lbl_finaliza = QLabel()
        self.lbl_finaliza.setText("FINALIZA PEDIDO")
        self.lbl_finaliza.setFont(QFont("Times", 12, QFont.Bold))
        self.lbl_finaliza.setAlignment(Qt.AlignCenter)
        # self.lbl_total.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        layout.addWidget(self.lbl_finaliza)

        self.precoinput = QLineEdit()
        self.onlyFloat = QDoubleValidator()
        self.precoinput.setValidator(self.onlyFloat)
        self.precoinput.setPlaceholderText("Digite o valor recebido aqui - 'R$ 0,00'")
        self.precoinput.textChanged[str].connect(self.check_disable)
        layout.addWidget(self.precoinput)

        self.lbl_total = QLabel()
        self.lbl_total.setText(str(totaliza).replace(".", ","))
        self.lbl_total.setFont(QFont("Times", 42, QFont.Bold))
        self.lbl_total.setAlignment(Qt.AlignCenter)
        self.lbl_total.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        layout.addWidget(self.lbl_total)

        self.lbl_troco = QLabel()
        # self.lbl_troco.setText(str(totaliza))
        self.lbl_troco.setText("R$ 0,00")
        self.lbl_troco.setFont(QFont("Times", 42, QFont.Bold))
        self.lbl_troco.setAlignment(Qt.AlignCenter)
        self.lbl_troco.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        layout.addWidget(self.lbl_troco)

        self.buttonreceber = QPushButton("Receber", self)
        self.buttonreceber.setIcon(QIcon("Icones/dollars.png"))
        self.buttonreceber.setIconSize(QSize(40, 40))
        self.buttonreceber.setMinimumHeight(40)
        self.buttonreceber.clicked.connect(lambda: self.receber(totalizando))
        self.buttonreceber.setEnabled(False)
        layout.addWidget(self.buttonreceber)

        self.buttonfinalizar = QPushButton("Finalizar", self)
        self.buttonfinalizar.setIcon(QIcon("Icones/carrinho.png"))
        self.buttonfinalizar.setIconSize(QSize(40, 40))
        self.buttonfinalizar.setMinimumHeight(40)
        self.buttonfinalizar.clicked.connect(lambda: self.finalizar(n_caixa))
        layout.addWidget(self.buttonfinalizar)

        recebido = 0

        totalizando = fechamento

        self.setLayout(layout)
        self.show()

    def receber(self, totalizando):
        recebido = float(self.precoinput.text().replace(",", "."))

        self.lbl_total.setText(
            (str("Total = R$ {0:.2f}".format(totalizando).replace(".", ",")))
        )
        troco = recebido - totalizando
        self.lbl_troco.setText(
            (str("Troco = R$ {0:.2f}".format(troco)).replace(".", ","))
        )

    def check_disable(self):
        if self.precoinput.text():
            self.buttonreceber.setEnabled(True)
        else:
            self.buttonreceber.setEnabled(False)

    def finalizar(self, n_caixa):
        self.nr_caixa = n_caixa

        replay = QMessageBox.question(
            self,
            "Window close",
            "Tem certeza de que deseja finalizar a compra?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if replay == QMessageBox.Yes:
            self.cursor = conexao.banco.cursor()
            comando_sql = (
                "INSERT INTO estoque "
                "(idproduto, estoque, status, preco_compra)"
                "SELECT cod_produto, quantidade,'S', 0 "
                "FROM pedidocaixa as pc  "
                "WHERE  pc.nr_caixa =" + str(self.nr_caixa)
            )
            self.cursor.execute(comando_sql)
            conexao.banco.commit()

            replay2 = QMessageBox.question(
                self,
                "Window close",
                "Deseja imprimir um cupon?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if replay2 == QMessageBox.Yes:
                self.hide()

                self.printer()

            else:
                self.hide()
                dlg = telaprincipal()
                dlg.exec()

        return self.nr_caixa

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

        # Define o diretório onde deseja salvar o arquivo
        save_dir = "/home/bionico/Documentos/Projetos21/caixa/caixa2022/relatorios/"  # Substitua pelo caminho desejado

        # Combine o caminho do diretório com o nome do arquivo
        full_path = os.path.join(save_dir, pdf_filename)

        # doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        doc = SimpleDocTemplate(full_path, pagesize=letter)
        story = []

        styles = getSampleStyleSheet()

        # Cria um estilo personalizado para o cabeçalho centralizado
        styleH = styles["Heading1"]
        styleH.alignment = 1  # Defina o alinhamento para centralizar

        # Cabeçalho
        header_text = "Recibo"
        header = Paragraph(header_text, styleH)
        story.append(header)
        story.append(Spacer(1, 12))

        header = [
            "COD",
            "PRODUTO",
            "QTD.",
            "PREÇO",
            "SUBTOTAL",
        ]

        results = [header]

        for row in dados_lidos:
            subtotal = row[3] * row[2]  # Preço x Quantidade
            results.append(
                [str(row[0]), row[1], str(row[2]), str(row[3]), str(subtotal)]
            )

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

        # Adicione a tabela à história
        story.append(table)
        story.append(Spacer(1, 12))

        # Total do pedido
        total_text = f"Total do Pedido: R${total_pedido:.2f}"
        total_paragraph = Paragraph(total_text, styles["Normal"])
        story.append(total_paragraph)

        # Salvar o arquivo automaticamente
        doc.build(story)

        dlg = telaprincipal()
        dlg.exec()

        return pdf_filename


class ListPedidos(QMainWindow):
    def __init__(self):
        super(ListPedidos, self).__init__()
        self.setWindowIcon(QIcon("Icones/produtos.png"))

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PEDIDOS")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # criar uma tabela centralizada
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        # muda a cor da linha selecionada
        self.tableWidget.setAlternatingRowColors(True)
        # indica a quantidade de colunas
        self.tableWidget.setColumnCount(6)
        # define que o cabeçalho não seja alterado
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        # Estica conforme o conteudo da célula
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(
            (
                "Numero.Pedido",
                "Cod.Produto",
                "Descrição",
                "Quantidade",
                "total",
                "ultupdate",
            )
        )

        self.cursor = conexao.banco.cursor()

        sql = """ SELECT
                            nr_caixa,
                            cod_produto,
                            p.descricao,
                            quantidade,
                            valor_total,
                            ultupdate
                        FROM
                            pedidocaixa as pd
                        LEFT JOIN produtos as p
                        ON cod_produto = p.codigo

                    """

        where = """ where pd.ultupdate >= curdate()"""

        comando_sql = sql + where

        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()
        # result = self.cursor.fetchone()[0::]

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnCount(6)

        for i in range(0, len(result)):
            for j in range(0, 6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        # botões do menu

        btn_ac_refresch = QAction(
            QIcon("Icones/atualizar.png"), "Atualizar dados da Lista de Pedidos", self
        )
        btn_ac_refresch.triggered.connect(self.loaddatapedido)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        self.buscainput = QLineEdit()

        self.buscainput.setStatusTip("número do pedido")
        toolbar.addWidget(self.buscainput)

        self.soma_pedido = QLabel()
        toolbar.addWidget(self.soma_pedido)

        # creating a QDateEdit widget
        self.data = QDateEdit(self)
        d1 = QDate(2021, 1, 1)
        d2 = QDate(9999, 10, 10)
        self.data.setDateRange(d1, d2)
        toolbar.addWidget(self.data)

        self.data2 = QDateEdit(self)
        d1 = QDate(2021, 1, 1)
        d2 = QDate(9999, 10, 10)
        self.data2.setDateRange(d1, d2)
        self.data2.editingFinished.connect(
            lambda: (self.date_method(self.data, self.data2))
        )
        toolbar.addWidget(self.data2)

        btn_ac_busca = QAction(QIcon("Icones/pesquisa.png"), "Filtra pedidos", self)
        btn_ac_busca.triggered.connect(lambda: self.filtraPedidos(self.buscaNro()))
        btn_ac_busca.setStatusTip("Filtro")
        toolbar.addAction(btn_ac_busca)

        btn_ac_sair = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_sair.triggered.connect(self.fechar)
        toolbar.addAction(btn_ac_sair)

        self.show()
        # self.loaddatapedido()

    def date_method(self, data, data2):
        self.data_value = data.date().toPyDate()
        self.data_value2 = data2.date().toPyDate()

        self.cursor = conexao.banco.cursor()
        sql = """ SELECT
                        nr_caixa,
                        cod_produto,
                        p.descricao,
                        quantidade,
                        valor_total,
                        ultupdate
                    FROM
                        pedidocaixa as pdc
                    LEFT JOIN produtos as p ON cod_produto = p.codigo
                """

        where = ""
        if str(self.data_value):
            where = """ where pdc.ultupdate BETWEEN '{}' and '{}' """.format(
                self.data_value, self.data_value2
            )

        comando_sql = sql + where

        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnCount(6)

        pedido = []
        x = [list(result[x]) for x in range(len(result))]

        soma_pedido = 0
        for i in range(len(x)):
            pedido.append(x[i])
            soma_pedido += x[i][4]

        if (len(pedido)) == 0:
            pass

        else:
            for i in range(0, len(pedido)):
                for j in range(0, 6):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(pedido[i][j])))
        self.soma_pedido.setText(
            (str("Total R$ {0:.2f}".format(soma_pedido).replace(".", ",")))
        )

    def buscaNro(self):
        busca_nro_pedido = self.buscainput.text()
        return busca_nro_pedido

    def filtraPedidos(self, busca_nro_pedido):
        self.busca_nro_pedido = busca_nro_pedido
        try:
            self.cursor = conexao.banco.cursor()

            sql = """ SELECT
                                nr_caixa,
                                cod_produto,
                                p.descricao,
                                quantidade,
                                valor_total,
                                ultupdate
                            FROM
                                pedidocaixa
                            LEFT JOIN produtos as p ON cod_produto = p.codigo
                  """

            order = """ order by
                            ultupdate desc """

            where = ""
            if self.busca_nro_pedido != "":
                where = """ where nr_caixa = """ + self.busca_nro_pedido

            comando_sql = sql + where + order

            self.cursor.execute(comando_sql)
            result = self.cursor.fetchall()

            self.tableWidget.setRowCount(len(result))
            self.tableWidget.resizeRowsToContents()
            self.tableWidget.setColumnCount(6)

            pedido = []
            x = [list(result[x]) for x in range(len(result))]

            soma_pedido = 0
            for i in range(len(x)):
                pedido.append(x[i])
                soma_pedido += x[i][4]

            if (len(pedido)) == 0:
                pass

            else:
                for i in range(0, len(pedido)):
                    for j in range(0, 6):
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(str(pedido[i][j]))
                        )

            self.soma_pedido.setText(
                (str("Total R$ {0:.2f}".format(soma_pedido).replace(".", ",")))
            )

        except:
            print("Falhou ao tentar ler os dados da tabela")

    def loaddatapedido(self):
        self.cursor = conexao.banco.cursor()

        comando_sql = """ SELECT
                                   nr_caixa,
                                   cod_produto,
                                   p.descricao,
                                   quantidade,
                                   valor_total,
                                   ultupdate
                               FROM
                                   pedidocaixa
                               LEFT JOIN produtos as p
                               ON cod_produto = p.codigo
                               order by
                                   ultupdate desc
                           """
        self.cursor.execute(comando_sql)
        result = self.cursor.fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(6)

        x = [list(result[x]) for x in range(len(result))]

        soma_pedido = 0
        for i in range(len(x)):
            soma_pedido += x[i][4]

        for i in range(0, len(result)):
            for j in range(0, 6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

        self.soma_pedido.setText(
            (str("Total R$ {0:.2f}".format(soma_pedido).replace(".", ",")))
        )

    def showPedido(self):
        dlg = Show_pedidos()
        dlg.exec()

    def fechar(self):
        self.close()


class MainWindow(QMainWindow):
    """
    Tela principal onde eu chamo as telas de
    cadastro de clientes
    cadastro de Produtos
    """

    def __init__(self, w):
        super(MainWindow, self).__init__()

        self.label = QLabel(self)

        self.pixmap = QPixmap("img/fundo.jpg")
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(), self.pixmap.height())

        self.setWindowIcon(QIcon("Icones/perfil.png"))

        # cria um menu
        file_menu = self.menuBar().addMenu("&Arquivo")
        help_menu = self.menuBar().addMenu("&Ajuda")
        self.setCentralWidget(w)

        self.setWindowTitle("SCC - SISTEMA DE CONTROLE")
        self.setMinimumSize(800, 700)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # Adicionar rótulo de relógio à barra de status
        self.clock_label = QLabel(self.statusBar())
        self.statusBar().addPermanentWidget(self.clock_label)
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # botões do menu
        btn_ac_adduser = QAction(
            QIcon("Icones/clientes.png"), "Listar/Cadastrar Cliente", self
        )
        btn_ac_adduser.triggered.connect(self.listClientes)
        btn_ac_adduser.setStatusTip("Clientes")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_produto = QAction(
            QIcon("Icones/produtos2.png"), "Lista/Cadastrar Produtos", self
        )
        btn_ac_produto.triggered.connect(self.listProdutos)
        btn_ac_produto.setStatusTip("Produtos")
        toolbar.addAction(btn_ac_produto)

        btn_ac_estoque = QAction(
            QIcon("Icones/estoque.png"), "Lista/Cadastro Estoque", self
        )
        btn_ac_estoque.triggered.connect(self.listEstoque)
        btn_ac_estoque.setStatusTip("Estoque")
        toolbar.addAction(btn_ac_estoque)

        btn_ac_pedido = QAction(QIcon("Icones/produtos.png"), "Listar Pedidos", self)
        btn_ac_pedido.triggered.connect(self.listPedido)
        btn_ac_pedido.setStatusTip("Pedidos")
        toolbar.addAction(btn_ac_pedido)

        btn_ac_relatorio_fechamento = QAction(
            QIcon("Icones/relatorio.png"), "Relatório de fechamento", self
        )
        btn_ac_relatorio_fechamento.triggered.connect(self.relatorioFechamentocaixa)
        btn_ac_relatorio_fechamento.setStatusTip("Relatório de Fechamento")
        toolbar.addAction(btn_ac_relatorio_fechamento)

        btn_ac_fechar = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_fechar.triggered.connect(self.fechaTela)
        btn_ac_fechar.setStatusTip("Sair")
        toolbar.addAction(btn_ac_fechar)

        # Arquivo >> Adicionar
        adduser_action = QAction(
            QIcon("Icones/clientes.png"), "Listar/Cadastrar de Cliente", self
        )
        adduser_action.triggered.connect(self.listClientes)
        file_menu.addAction(adduser_action)

        btn_ac_produto = QAction(
            QIcon("Icones/produtos2.png"), "Listar/Cadastrar Produtos", self
        )
        btn_ac_produto.triggered.connect(self.listProdutos)
        file_menu.addAction(btn_ac_produto)

        btn_ac_pedido = QAction(QIcon("Icones/produtos.png"), "Listar Pedidos", self)
        btn_ac_pedido.triggered.connect(self.listPedido)
        file_menu.addAction(btn_ac_pedido)

        btn_ac_estoque = QAction(
            QIcon("Icones/estoque.png"), "Lista/Cadastro Estoque", self
        )
        btn_ac_estoque.triggered.connect(self.listEstoque)
        file_menu.addAction(btn_ac_estoque)

        btn_ac_relatorio_fechamento = QAction(
            QIcon("Icones/relatorio.png"), "Relatório de fechamento", self
        )
        btn_ac_relatorio_fechamento.triggered.connect(self.relatorioFechamentocaixa)
        file_menu.addAction(btn_ac_relatorio_fechamento)

        btn_ac_Cupon = QAction(QIcon("Icones/impressora.png"), "Imprimir Cupon", self)
        btn_ac_Cupon.triggered.connect(self.cupon)
        file_menu.addAction(btn_ac_Cupon)

        btn_ac_Backup = QAction(QIcon("Icones/backup.png"), "Bakup", self)
        btn_ac_Backup.triggered.connect(self.backup_manual)
        file_menu.addAction(btn_ac_Backup)

        btn_ac_fechar = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_fechar.setShortcut("Ctrl+Q")
        btn_ac_fechar.triggered.connect(self.fechaTela)
        file_menu.addAction(btn_ac_fechar)

        about_action = QAction(QIcon("Icones/sobre-nos.png"), "Desenvolvedores", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        # self.show()
        self.showFullScreen()

    def update_time(self):
        current_time = QTime.currentTime()
        time_text = current_time.toString("hh:mm:ss")
        self.clock_label.setText("Hora: " + time_text)

    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    def listClientes(self):
        dlg = ListClientes()
        dlg.exec()

    def listProdutos(self):
        dlg = ListProdutos()
        dlg.exec()

    def listPedido(self):
        dlg = ListPedidos()
        dlg.exec()

    def relatorioFechamentocaixa(self):
        """Chama script externo"""

        import subprocess

        # Caminho para o script externo
        caminho_script_externo = "relatorio_fechamento3.py"

        # Chamar o script externo
        subprocess.run(["python3", caminho_script_externo])

    def listEstoque(self):
        dlg = ListEstoque()
        dlg.exec()

    def cupon(self):
        dlg = Imprimir()
        dlg.exec_()

    def backup_manual(self):
        dlg = DatabaseBackupApp()
        dlg.exec_()

    def cupom_pdf(self):
        cursor = conexao.banco.cursor()
        comando_SQL = "SELECT * FROM produtos"
        cursor.execute(comando_SQL)
        dados_lidos = cursor.fetchall()
        y = 0
        pdf = canvas.Canvas("Lista de Produtos.pdf")
        pdf.setFont("Times-Bold", 18)
        pdf.drawString(200, 800, "Produtos: ")
        pdf.setFont("Times-Bold", 12)

        pdf.drawString(10, 750, "ID")
        pdf.drawString(50, 750, "CODIGO")
        pdf.drawString(110, 750, "PRODUTO")
        pdf.drawString(310, 750, "PREÇO")
        pdf.drawString(410, 750, "CATEGORIA")

        for i in range(0, len(dados_lidos)):
            y += 50
            pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
            pdf.drawString(50, 750 - y, str(dados_lidos[i][1]))
            pdf.drawString(110, 750 - y, str(dados_lidos[i][2]))
            pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
            pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

        pdf.save()

        valor = 0

    def fechaTela(self, event):
        replay = QMessageBox.question(
            self,
            "Window close",
            "Tem certeza de que deseja sair?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if replay == QMessageBox.Yes:
            sys.exit()

        else:
            event.ignore()


class DatabaseBackupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Backup do Banco de Dados MySQL")
        self.setGeometry(100, 100, 400, 150)

        self.backup_button = QPushButton("Realizar Backup")
        self.backup_button.clicked.connect(self.backup_database)

        self.label = QLabel("Status: Aguardando Backup")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.backup_button)
        self.setLayout(layout)

        self.show()

    def backup_database(self):
        try:
            # Use as informações de conexão do arquivo conexão.py
            connection = conexao.banco

            if connection.is_connected():
                cursor = connection.cursor()

                try:
                    # Defina o diretório de destino do backup
                    backup_directory = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)), "backup"
                    )

                    # Crie o diretório de backup, se não existir
                    if not os.path.exists(backup_directory):
                        os.makedirs(backup_directory)

                    # Nomeie o arquivo de backup com a data e hora atual
                    backup_file = os.path.join(
                        backup_directory,
                        f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql",
                    )

                    # Use o utilitário mysqldump para fazer o backup do banco de dados
                    backup_config = {
                        "user": connection.user,
                        "passwd": connection._password,
                        "host": connection._host,
                        "database": connection.database,
                    }
                    mysqldump_cmd = f"mysqldump -u {backup_config['user']} -p{backup_config['passwd']} -h {backup_config['host']} {backup_config['database']} > {backup_file}"
                    os.system(mysqldump_cmd)

                    self.label.setText(f"Status: Backup concluído em {backup_file}")
                    QMessageBox.information(
                        self,
                        "Backup Concluído",
                        "O backup foi concluído com sucesso!",
                    )

                except Exception as e:
                    self.label.setText(f"Status: Erro ao fazer o backup - {str(e)}")
                    QMessageBox.critical(
                        self,
                        "Erro de Backup",
                        f"Ocorreu um erro ao fazer o backup: {str(e)}",
                    )

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class LoginForm(QDialog):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setWindowTitle("Login")
        self.resize(500, 120)

        layout = QGridLayout()

        label_nome = QLabel('<font size="4"> Usuário </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText("Nome de Usuário")
        layout.addWidget(label_nome, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_senha = QLabel('<font size="4"> Senha </font>')
        self.lineEdit_senha = QLineEdit()
        self.lineEdit_senha.setPlaceholderText("Digite sua senha aqui")
        self.lineEdit_senha.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_senha, 1, 0)
        layout.addWidget(self.lineEdit_senha, 1, 1)

        # creating progress bar
        self.pbar = QProgressBar(self)
        layout.addWidget(self.pbar, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        button_login = QPushButton("Login")
        button_login.setStyleSheet("font-size: 20px; height: 30px;")
        button_login.clicked.connect(self.check_senha)
        layout.addWidget(button_login, 3, 0, 1, 1)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

    def check_senha(self):
        msg = QMessageBox()

        usuario = self.lineEdit_username.text()
        senha = self.lineEdit_senha.text()
        self.cursor = conexao.banco.cursor()
        comando_sql = "SELECT senha FROM usuarios WHERE nome ='{}' ".format(usuario)

        try:
            self.cursor.execute(comando_sql)
            senha_bd = self.cursor.fetchall()

        except Exception as e:
            msg.setText("Credenciais Incorretas")
            msg.exec_()

        if senha == senha_bd[0][0]:
            for i in range(101):
                time.sleep(0.01)
                self.pbar.setValue(i)
            self.hide()
            telaprincipal()
            msg.setText("Sucesso")
            msg.exec_()
            conexao.banco.close()
        else:
            msg.setText("Credenciais Incorretas")
            msg.exec_()


def telaprincipal():
    w = DataEntryForm()
    dlg = MainWindow(w)
    dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

if QDialog.Accepted:
    form = LoginForm()
    form.show()

sys.exit((app.exec_()))
