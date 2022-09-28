
class CustomTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(QAbstractTableModel, self).__init__()

        self.meus_dados = data[0]
        self.minhas_colunas = data[1]

        self.load_data(self.meus_dados)

    def load_data(self, dados):
        self.numero_linhas = len(dados)
        self.numero_colunas = len(dados[0])

    def rowCount(self, parent=QModelIndex()):
        return self.numero_linhas

    def columnCount(self, parent=QModelIndex()):
        return self.numero_colunas

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.minhas_colunas[section].upper()
        else:
            return section

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return self.meus_dados[row][column]
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignLeft
        elif role == Qt.BackgroundColorRole:
            return QColor(Qt.white)

        return None


class ListPedidos2(QMainWindow):
    def __init__(self):
        super(ListPedidos, self).__init__()

        # self.setWindowIcon(QIcon('Icones/produtos.png'))

        # self.setWindowTitle("SCC - SISTEMA DE CONTROLE DE PEDIDOS")
        self.setMinimumSize(800, 600)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        # criar uma tabela c
        self.tableView = QTableView()

        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.titulos = self.tableView.horizontalHeader()
        self.titulos.setSectionResizeMode(QHeaderView.Interactive)

        dados = self.consulta_pedidos()

        self.model = CustomTableModel(dados)
        self.tableView.setModel(self.model)
        self.setCentralWidget(self.tableView)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        # botões do menu

        btn_ac_refresch = QAction(
            QIcon("Icones/atualizar.png"), "Atualizar dados da Lista de Pedidos", self)
        # btn_ac_refresch.triggered.connect(self.loaddatapedido)
        btn_ac_refresch.setStatusTip("Atualizar")
        toolbar.addAction(btn_ac_refresch)

        self.buscainput = QLineEdit()
        # self.buscainput.textChanged.connect(self.search_pedidos)
        toolbar.addWidget(self.buscainput)

        btn_ac_busca = QAction(
            QIcon("Icones/pesquisa.png"), "Filtra pedidos", self)
        # btn_ac_busca.triggered.connect(self.filtraPedidos)
        # btn_ac_busca.triggered.connect(lambda: self.filtraPedidos(nro_pedido))
        btn_ac_busca.triggered.connect(
            lambda: self.search_pedidos(self.buscainput.text()))
        btn_ac_busca.setStatusTip("Filtro")
        toolbar.addAction(btn_ac_busca)

        self.show()
        # self.loaddatapedido()

    def search_pedidos2(self):
        dados = self.consulta_pedidos()
        model = QStandardItemModel(len(dados), 1)
        model.setHorizontalHeaderLabels(['Pedidos Filtrados'])

        for row, pedidos in enumerate(dados):
            for j, data in enumerate(pedidos):
                item = QStandardItem()
                item.setData(data, Qt.DisplayRole)
                model.setItem(row, j, item)

        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(model)
        # filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.filter_proxy_model.setFilterRegExp
        self.tableView.setModel(self.filter_proxy_model)


# https://stackoverflow-com.translate.goog/questions/20693470/search-find-functionality-in-qtableview?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt-BR&_x_tr_pto=wapp


    def search_pedidos(self, text, column=0):
        model = self.tableView.model()
        # indexes = self.tableView.selectionModel().selectedIndexes()
        start = model.index(0, column)
        matches = model.match(
            start, Qt.DisplayRole,
            text, 1, Qt.MatchContains)
        if matches:
            index = matches[0]
            # index.row(), index.column()
            self.tableView.selectionModel().select(
                index, QItemSelectionModel.Select)
    # ATUALIZAR :

    # O método acima encontrará a primeira célula que contém o
    # texto fornecido e a selecionará. Se você quisesse encontrar a próxima
    # célula que correspondesse, start precisaria ser definido para o índice
    # apropriado da seleção atual (se houver). Isso pode ser obtido com:
    #     indexes = self.table.selectionModel().selectedIndexes()

    def consulta_pedidos(self):

        self.cursor = conexao.banco.cursor()

        comando_sql = """ SELECT 
                            idpedidocaixa,
                            cod_produto, 
                            p.descricao,
                            quantidade, 
                            preco,
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
        resultado = self.cursor.fetchall()

        # pega o numero de colunas
        num_colunas = len(self.cursor.description)
        nome_colunas = [i[0] for i in self.cursor.description]
        dados = (resultado, nome_colunas)

        return dados
