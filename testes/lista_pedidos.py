from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDateEdit,
    QLabel,
    QLineEdit,
    QMainWindow,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
)

import conexao


class ListPedidos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PEDIDOS")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)

        self.setupTableWidget()
        self.setupToolbar()
        self.setupStatusBar()

        self.loaddatapedido()
        self.show()

    def setupTableWidget(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(6)
        header_labels = (
            "Numero.Pedido",
            "Cod.Produto",
            "Descrição",
            "Quantidade",
            "total",
            "ultupdate",
        )
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.setCentralWidget(self.tableWidget)

    def setupToolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        btn_ac_refresch = QAction(
            QIcon("Icones/atualizar.png"), "Atualizar dados da Lista de Pedidos", self
        )
        btn_ac_refresch.triggered.connect(self.loaddatapedido)
        toolbar.addAction(btn_ac_refresch)

        self.buscainput = QLineEdit()
        toolbar.addWidget(self.buscainput)

        self.soma_pedido = QLabel()
        toolbar.addWidget(self.soma_pedido)

        self.data = QDateEdit(self)
        self.data.setDateRange(QDate(2021, 1, 1), QDate(9999, 10, 10))
        toolbar.addWidget(self.data)

        self.data2 = QDateEdit(self)
        self.data2.setDateRange(QDate(2021, 1, 1), QDate(9999, 10, 10))
        self.data2.editingFinished.connect(
            lambda: self.date_method(self.data, self.data2)
        )
        toolbar.addWidget(self.data2)

        btn_ac_busca = QAction(QIcon("Icones/pesquisa.png"), "Filtra pedidos", self)
        btn_ac_busca.triggered.connect(lambda: self.filtraPedidos(self.buscaNro()))
        toolbar.addAction(btn_ac_busca)

        btn_ac_sair = QAction(QIcon("Icones/sair.png"), "Sair", self)
        btn_ac_sair.triggered.connect(self.fechar)
        toolbar.addAction(btn_ac_sair)

    def setupStatusBar(self):
        self.setStatusBar(QStatusBar())

    def loaddatapedido(self):
        sql = """
            SELECT
                nr_caixa,
                cod_produto,
                p.descricao,
                quantidade,
                valor_total,
                ultupdate
            FROM
                pedidocaixa
            LEFT JOIN produtos as p ON cod_produto = p.codigo
            ORDER BY
                ultupdate DESC
        """

        self.executeAndPopulateTable(sql)

    def executeAndPopulateTable(self, sql):
        self.cursor = conexao.banco.cursor()
        self.cursor.execute(sql)
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

        self.soma_pedido.setText(f"Total R$ {soma_pedido:.2f}".replace(".", ","))

    def date_method(self, data, data2):
        self.data_value = data.date().toPyDate()
        self.data_value2 = data2.date().toPyDate()

        sql = """
            SELECT
                nr_caixa,
                cod_produto,
                p.descricao,
                quantidade,
                valor_total,
                ultupdate
            FROM
                pedidocaixa as pdc
            LEFT JOIN produtos as p ON cod_produto = p.codigo
            WHERE pdc.ultupdate BETWEEN %s AND %s
        """

        self.executeAndPopulateTable(sql, (self.data_value, self.data_value2))

    def buscaNro(self):
        return self.buscainput.text()

    def filtraPedidos(self, busca_nro_pedido):
        sql = """
            SELECT
                nr_caixa,
                cod_produto,
                p.descricao,
                quantidade,
                valor_total,
                ultupdate
            FROM
                pedidocaixa
            LEFT JOIN produtos as p ON cod_produto = p.codigo
            WHERE nr_caixa = %s
            ORDER BY
                ultupdate DESC
        """

        self.executeAndPopulateTable(sql, (busca_nro_pedido,))

    def fechar(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = ListPedidos()
    app.exec_()
