
import sys

from PyQt5.QtWidgets import *


class CadastroProdutos(QWidget):
    """
        Define uma nova janela onde cadastramos os clientes
    """

    def __init__(self, *args, **kwargs):
        super(CadastroProdutos, self).__init__(*args, **kwargs)

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # Configurações do titulo da Janela
        self.setWindowTitle("Add Produto :")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Descição do Produto :")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        layout = QHBoxLayout()
        layoutV = QVBoxLayout()

        self.codigoean = QLineEdit()
        self.codigoean.setPlaceholderText("Código")
        layout.addWidget(self.codigoean)

        self.descricaoinput = QLineEdit()
        self.descricaoinput.setPlaceholderText("Descrição")
        layout.addWidget(self.descricaoinput)

        # Insere o ramo ou tipo /
        self.uninput = QComboBox()
        self.uninput.addItem("UN")
        self.uninput.addItem("PÇ")
        self.uninput.addItem("KG")
        self.uninput.addItem("LT")
        self.uninput.addItem("PT")
        self.uninput.addItem("CX")
        layout.addWidget(self.uninput)

        self.ncminput = QLineEdit()
        self.ncminput.setPlaceholderText("NCM")
        layout.addWidget(self.ncminput)

        self.precocusto = QLineEdit()
        self.precocusto.setPlaceholderText("Preço Custo.")
        layout.addWidget(self.precocusto)

        self.precoinput = QLineEdit()
        self.precoinput.setPlaceholderText("Preço.")
        grid_layout.addWidget(self.precoinput)

        self.button = QPushButton()
        self.button.setText("Registrar")
        grid_layout.addWidget(self.button)

        self.button.clicked.connect(self.addproduto)

        # layout.addWidget(self.button)
        # self.setLayout(layout)

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

        descricao = self.descricaoinput.text()
        ncm = self.ncminput.text()
        un = self.uninput.itemText(self.uninput.currentIndex())
        preco = self.precoinput.text()

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


root = QApplication(sys.argv)
app = CadastroProdutos()
app.show()
sys.exit(root.exec_())
