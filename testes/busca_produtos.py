dado o seuinte script permita que o usuario consiga auto completar
o campo codigo do produto ou o campo descrição do produto, através
da consulta ao banco de dados apresentado. mantenha as caracteristicas 
principais do programa e apresente o codigo completo.

class DataEntryForm(QWidget):
    def __init__(self):
        super().__init__()

        self.cursor = conexao.banco.cursor()
        consulta_sql = "SELECT * FROM clientes"
        self.cursor.execute(consulta_sql)
        result = self.cursor.fetchall()
        self.close()

        self.cursor = conexao.banco.cursor()

        consulta_prod = """SELECT p.codigo, p.descricao, p.preco, p.ncm, p.un FROM produtos as p
                            inner join controle_clientes.estoque as e
                            where e.status = '{}'
                            and e.estoque > '{}'
                            and e.idproduto = p.codigo group by p.codigo""".format(
            "E", 0
        )        


clientes = []
        for i in range(len(result)):
            if result[i][2]:
                clientes.append(result[i][2])

        self.lineEditCliente = QLineEdit()
        self.lineEditCliente.setPlaceholderText("Nome / Razão")
        self.model = QStandardItemModel()
        self.model = clientes
        completer = QCompleter(self.model, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEditCliente.setCompleter(completer)
        self.lineEditCliente.editingFinished.connect(self.addCliente)
        self.lineEditCliente.setEnabled(False)
        self.layoutRight.addWidget(self.lineEditCliente)

        produtos = []
        self.model_prod = QStandardItemModel()

        for row in result_prod:
            item = QStandardItem(f"{row[0]} - {row[1]}")
            self.model_prod.appendRow(item)

        self.lineEditCode = QLineEdit()
        self.lineEditCode.setPlaceholderText("Código do Produto")

        self.model = produtos
        completer_prod = QCompleter(self.model_prod, self)
        completer_prod.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEditCode.setCompleter(completer_prod)
        self.lineEditCode.editingFinished.connect(self.addProdutos)
        self.layoutRight.addWidget(self.lineEditCode)

        for i in range(len(result_prod)):
            if result_prod[i][1]:
                produtos.append(result_prod[i][1])

        self.lineEditDescription = QLineEdit()
        self.lineEditDescription.setPlaceholderText("Descrição / Produto")
        self.lineEditDescription.setCompleter(completer_prod)
        self.lineEditDescription.editingFinished.connect(self.addProdutos)
        self.layoutRight.addWidget(self.lineEditDescription)

def addProdutos(self):
        self.cursor = conexao.banco.cursor()
        consulta_prod = "SELECT * FROM produtos"
        self.cursor.execute(consulta_prod)
        result_prod = self.cursor.fetchall()

        entryItem = self.lineEditDescription.text()
        selected_item = entryItem.split(" - ")[
            0
        ]  # Extrai o código do produto selecionado
        print(f"Codigo selecionado AQUI: {selected_item}")

        for row in result_prod:
            if str(row[0]) == selected_item or str(row[1]) == entryItem:
                self.codigo = row[0]
                self.preco = row[2]
                self.TOTAL += float(self.preco)
                self.lineEditPrice.setText(str(self.preco))