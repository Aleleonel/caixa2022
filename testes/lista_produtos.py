from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QMainWindow,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
)

import conexao


class ListProdutos(QMainWindow):
    def __init__(self):
        super(ListProdutos, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PRODUTOS")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.setup_table_widget()
        self.setup_toolbar()

        self.show()

    def setup_table_widget(self):
        self.tableWidget = QTableWidget(self)
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(
            ("Codigo", "Descrição", "NCM", "UN", "Preço Venda")
        )

    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        actions = [
            ("Add Produto", "Icones/add.png", self.cadProdutos),
            ("Atualizar", "Icones/atualizar.png", self.loaddata),
            ("Deletar", "Icones/deletar.png", self.delete),
            ("Pesquisar", "Icones/pesquisa.png", self.searchProduto),
            ("Sair", "Icones/sair.png", self.fechar),
        ]

        for label, icon_path, function in actions:
            action = QAction(QIcon(icon_path), label, self)
            action.triggered.connect(function)
            toolbar.addAction(action)

    def loaddata(self):
        with conexao.banco.cursor() as cursor:
            comando_sql = "SELECT codigo, descricao, ncm, un, preco FROM controle_clientes.produtos"
            cursor.execute(comando_sql)
            result = cursor.fetchall()

        self.tableWidget.setRowCount(len(result))

        for i, row_data in enumerate(result):
            for j, cell_data in enumerate(row_data):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(cell_data)))

    def cadProdutos(self):
        dlg = CadastroProdutos()
        dlg.exec_()
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


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = ListProdutos()
    sys.exit(app.exec_())
