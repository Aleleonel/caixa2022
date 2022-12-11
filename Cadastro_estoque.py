import sys

from PyQt5.QtWidgets import *

import conexao


class CadastroEstoque(QDialog):
    """
        Define uma nova janela onde cadastramos os produtos
        no estoque
    """

    def __init__(self, *args, **kwargs):
        super(CadastroEstoque, self).__init__(*args, **kwargs)

        self.conexao_banco(self)

        self.createTopLeftGroupBox()
        self.createGroupBoxSalvar()
        self.createGroupBox()
        self.createEndercoGroupBox()

        self.QBtn = QPushButton()
        self.QBtn.setText("Registrar")

        # Configurações do titulo da Janela
        self.setWindowTitle("CADASTRO DE PRODUTOS EM ESTOQUE")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        def conexao_banco(self):
            self.cursor = conexao.banco.cursor()
            consulta_sql = "SELECT * FROM produtos"
            self.cursor.execute(consulta_sql)
            result = self.cursor.fetchall()

        def createGroupBox(self):
            self.GroupBox2 = QGroupBox()
            layout = QHBoxLayout()

            # Insere o ramo ou tipo /
            self.codigoinput = QComboBox()
            busca = []
            for row in range(len(result)):
                busca.append(str(result[row][0]))
            for i in range(len(busca)):
                self.codigoinput.addItem(str(busca[i]))

            layout.addWidget(self.codigoinput)

            self.QBtn.clicked.connect(self.addproduto)

            self.statusinput = QLineEdit()
            self.statusinput.setPlaceholderText("E")
            layout.addWidget(self.statusinput)

#         # Insere o ramo ou tipo /

#         self.descricaoinput = QLineEdit()
#         self.descricaoinput.setPlaceholderText("Descrição")
#         layout.addWidget(self.descricaoinput)

#         self.precoinput = QLineEdit()
#         self.precoinput.setPlaceholderText("Preço de Compra")
#         layout.addWidget(self.precoinput)

#         self.qtdinput = QLineEdit()
#         self.qtdinput.setPlaceholderText("Quantidade")
#         layout.addWidget(self.qtdinput)

#         layout.addWidget(self.QBtn)
#         self.setLayout(layout)

#     def addproduto(self):
#         """
#         captura as informações digitadas
#         no COMBOBOX e armazena nas variaveis
#         :return:
#         codigo = ""
#         quantidade = ""
#         preco = ""
#         status = "E"
#         E da entrada na tabela estoque
#         e preço de compra
#         """
#         self.cursor = conexao.banco.cursor()
#         consulta_sql = ("SELECT * FROM produtos WHERE codigo =" + str(self.codigoinput.itemText(
#             self.codigoinput.currentIndex())))
#         self.cursor.execute(consulta_sql)
#         valor_codigo = self.cursor.fetchall()

#         for i in range(len(valor_codigo)):
#             dados_lidos = valor_codigo[i][1]

#         codigo = ""
#         quantidade = ""
#         preco = ""
#         status = "E"

#         codigo = self.codigoinput.itemText(self.codigoinput.currentIndex())
#         self.descricaoinput.setText(dados_lidos)
#         preco = self.precoinput.text()
#         quantidade = self.qtdinput.text()

#         try:
#             self.cursor = conexao.banco.cursor()
#             comando_sql = "INSERT INTO estoque (idproduto, estoque, status, preco_compra)" \
#                           "VALUES (%s, %s, %s, %s)"
#             dados = codigo, quantidade, status, preco
#             self.cursor.execute(comando_sql, dados)
#             conexao.banco.commit()
#             self.cursor.close()

#             QMessageBox.information(
#                 QMessageBox(), 'Cadastro', 'Dados inseridos com sucesso!')
#             self.close()

#         except Exception:

#             QMessageBox.warning(
#                 QMessageBox(), 'aleleonel@gmail.com', 'A inserção falhou!')


# class CadastroEstoque(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(CadastroEstoque, self).__init__(*args, **kwargs)

#         disableWidgetsCheckBox = QCheckBox("&Disable widgets")

#         self.createTopLeftGroupBox()
#         self.createGroupBoxSalvar()
#         self.createGroupBox()
#         self.createEndercoGroupBox()

#         disableWidgetsCheckBox.toggled.connect(self.GroupBox1.setDisabled)
#         disableWidgetsCheckBox.toggled.connect(self.GroupBox2.setDisabled)
#         disableWidgetsCheckBox.toggled.connect(self.GroupBox3.setDisabled)
#         disableWidgetsCheckBox.toggled.connect(self.GroupBox4.setDisabled)

#         topLayout = QHBoxLayout()
#         topLayout.addStretch(1)
#         topLayout.addWidget(disableWidgetsCheckBox)

#         mainLayout = QGridLayout()
#         mainLayout.addLayout(topLayout, 0, 0, 1, 2)
#         mainLayout.addWidget(self.GroupBox1, 1, 0, 1, 2)
#         mainLayout.addWidget(self.GroupBox2, 2, 0, 1, 2)
#         mainLayout.addWidget(self.GroupBox3, 4, 0, 1, 2)
#         mainLayout.addWidget(self.GroupBox4, 3, 0, 1, 2)
#         mainLayout.setRowStretch(1, 1)
#         mainLayout.setRowStretch(2, 1)
#         mainLayout.setColumnStretch(0, 1)
#         mainLayout.setColumnStretch(1, 1)
#         self.setLayout(mainLayout)

#         self.setWindowTitle("CADASTRO DE PRODUTOS EM ESTOQUE")

#     def createGroupBox(self):
#         self.GroupBox2 = QGroupBox()

#         layout = QHBoxLayout()

#         self.cpfinput = QLineEdit()
#         self.cpfinput.setPlaceholderText("Cpf")

#         self.rginput = QLineEdit()
#         self.rginput.setPlaceholderText("R.G")

#         self.mobileinput = QLineEdit()
#         self.mobileinput.setPlaceholderText("Telefone NO.")

#         layout.addWidget(self.cpfinput)
#         layout.addWidget(self.rginput)

#         layout.addWidget(self.mobileinput)

#         layout.addStretch(1)
#         self.GroupBox2.setLayout(layout)

#     def createTopLeftGroupBox(self):
#         self.GroupBox1 = QGroupBox("Cadastro de Clientes")

#         layout = QVBoxLayout()

#         # Insere o ramo ou tipo /
#         self.branchinput = QComboBox()
#         self.branchinput.addItem("Pessoa Física")
#         self.branchinput.addItem("Pessoa Jurídica")

#         self.nameinput = QLineEdit()
#         self.nameinput.setPlaceholderText("Nome / Razão")

#         layout.addWidget(self.branchinput)
#         layout.addWidget(self.nameinput)

#         layout.addStretch(1)
#         self.GroupBox1.setLayout(layout)

#     def createEndercoGroupBox(self):
#         self.GroupBox4 = QGroupBox()

#         layout = QVBoxLayout()

#         self.addressinput = QLineEdit()
#         self.addressinput.setPlaceholderText("Logradouro")

#         self.bairro = QLineEdit()
#         self.bairro.setPlaceholderText("Bairro")

#         self.addresscomplemento = QLineEdit()
#         self.addresscomplemento.setPlaceholderText("Complemento")

#         self.addresscidade = QLineEdit()
#         self.addresscidade.setPlaceholderText("Cidade")

#         self.cep = QLineEdit()
#         self.cep.setPlaceholderText("CEP")

#         self.ederecoNumero = QLineEdit()
#         self.ederecoNumero.setPlaceholderText("Nr.")

#         layout.addWidget(self.addressinput)
#         layout.addWidget(self.bairro)
#         layout.addWidget(self.addresscomplemento)
#         layout.addWidget(self.ederecoNumero)
#         layout.addWidget(self.cep)
#         layout.addWidget(self.addresscidade)

#         layout.addStretch(1)
#         self.GroupBox4.setLayout(layout)

#     def createGroupBoxSalvar(self):
#         self.GroupBox3 = QGroupBox("Salvar Cadastro")

#         self.defaultPushButton = QPushButton("Salvar")
#         self.defaultPushButton.setDefault(True)
#         self.defaultPushButton.clicked.connect(self.addcliente)

#         self.defaultPushButton2 = QPushButton(self)
#         self.defaultPushButton2.setDefault(True)
#         self.defaultPushButton2.setIcon(QIcon("Icones/sair.png"))
#         self.defaultPushButton2.setIconSize(QSize(20, 20))
#         self.defaultPushButton2.setMinimumHeight(25)
#         self.defaultPushButton2.clicked.connect(self.closeCadastro)

#         layout = QGridLayout()
#         layout.addWidget(self.defaultPushButton, 1, 0, 1, 2)
#         layout.addWidget(self.defaultPushButton2, 2, 0, 1, 2)
#         layout.setRowStretch(5, 1)
#         self.GroupBox3.setLayout(layout)


root = QApplication(sys.argv)
app = CadastroEstoque()
app.show()
sys.exit(root.exec_())
