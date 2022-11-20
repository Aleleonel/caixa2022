
import sys

from PyQt5.QtWidgets import *


class CadastroClientes(QDialog):
    def __init__(self, *args, **kwargs):
        super(CadastroClientes, self).__init__(*args, **kwargs)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createGroupBoxSalvar()
        self.createGroupBox()
        self.createEndercoGroupBox()

        disableWidgetsCheckBox.toggled.connect(self.GroupBox1.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.GroupBox2.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.GroupBox3.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.GroupBox4.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)
        topLayout.addWidget(disableWidgetsCheckBox)

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

        self.cpfinput = QLineEdit()
        self.cpfinput.setPlaceholderText("Cpf")

        self.rginput = QLineEdit()
        self.rginput.setPlaceholderText("R.G")

        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Telefone NO.")

        layout.addWidget(self.cpfinput)
        layout.addWidget(self.rginput)

        layout.addWidget(self.mobileinput)

        layout.addStretch(1)
        self.GroupBox2.setLayout(layout)

    def createTopLeftGroupBox(self):
        self.GroupBox1 = QGroupBox("Cadastro de Clientes")

        layout = QVBoxLayout()

        # Insere o ramo ou tipo /
        self.branchinput = QComboBox()
        self.branchinput.addItem("Pessoa Física")
        self.branchinput.addItem("Empresa")

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Nome / Razão")

        layout.addWidget(self.branchinput)
        layout.addWidget(self.nameinput)

        layout.addStretch(1)
        self.GroupBox1.setLayout(layout)

    def createEndercoGroupBox(self):
        self.GroupBox4 = QGroupBox()

        layout = QVBoxLayout()

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Logradouro")

        self.bairro = QLineEdit()
        self.bairro.setPlaceholderText("Bairro")

        self.addresscomplemento = QLineEdit()
        self.addresscomplemento.setPlaceholderText("Complemento")

        self.cep = QLineEdit()
        self.cep.setPlaceholderText("CEP")

        self.ederecoNumero = QLineEdit()
        self.ederecoNumero.setPlaceholderText("Nr.")

        layout.addWidget(self.addressinput)
        layout.addWidget(self.bairro)
        layout.addWidget(self.addresscomplemento)
        layout.addWidget(self.ederecoNumero)
        layout.addWidget(self.cep)

        layout.addStretch(1)
        self.GroupBox4.setLayout(layout)

    def createGroupBoxSalvar(self):
        self.GroupBox3 = QGroupBox("Salvar Cadastro")

        self.defaultPushButton = QPushButton("Salvar")
        self.defaultPushButton.setDefault(True)
        # self.defaultPushButton.clicked.connect(self.addproduto)

        self.defaultPushButton2 = QPushButton("Fechar")
        self.defaultPushButton2.setDefault(True)
        self.defaultPushButton2.clicked.connect(self.closeCadastro)

        layout = QGridLayout()
        layout.addWidget(self.defaultPushButton, 1, 0, 1, 2)
        layout.addWidget(self.defaultPushButton2, 2, 0, 1, 2)
        layout.setRowStretch(5, 1)
        self.GroupBox3.setLayout(layout)

    def closeCadastro(self):
        self.close()


root = QApplication(sys.argv)
app = CadastroClientes()
app.show()
sys.exit(root.exec_())
