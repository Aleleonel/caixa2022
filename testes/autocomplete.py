from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QCompleter, QGroupBox, QLabel, QLineEdit, QWidget


class SuaClasse(QWidget):
    def __init__(self):
        super().__init__()

        # Conexão com o banco e execução da consulta
        self.cursor = conexao.banco.cursor()
        sql = "SELECT codigo, descricao, ncm, un, preco, est.preco_compra FROM produtos INNER JOIN controle_clientes.estoque as est WHERE sua_condicao_aqui"
        self.cursor.execute(sql)
        result_prod = self.cursor.fetchall()

        # Criação da lista de produtos
        produtos = [item[1] for item in result_prod if item[1]]

        # Criação dos widgets
        self.GroupBox2 = QGroupBox(self)
        self.label_descricao = QLabel("Descrição", self.GroupBox2)
        self.label_descricao.setAlignment(Qt.AlignLeft)
        self.descricao = QLineEdit(self.GroupBox2)
        self.descricao.setPlaceholderText("Descrição / Produto")

        # Configuração do autocompletar
        self.model_prod = QStandardItemModel()
        for produto in produtos:
            item = QStandardItem(produto)
            self.model_prod.appendRow(item)

        completer_prod = QCompleter(self.model_prod, self)
        completer_prod.setCaseSensitivity(Qt.CaseInsensitive)
        self.descricao.setCompleter(completer_prod)
        self.descricao.returnPressed.connect(self.consultaProdutolist)

        # Configuração de tamanho
        self.descricao.setFixedSize(447, 25)

    def consultaProdutolist(self):
        # Implemente a ação desejada ao pressionar Enter na caixa de texto de descrição
        pass
