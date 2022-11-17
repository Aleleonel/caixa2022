class Imprimir(QWidget):
    ''' Imprime usando uma box com opções de impressora e visualizações'''

    def __init__(self, n_caixa):
        super(Imprimir, self).__init__()
        self.black = "#000000"
        self.yellow = "#cfb119"
        self.setStyleSheet(
            f"background-color: {self.black}; color: {self.yellow};")

        self.nr_caixa = n_caixa

        self.vbox = QVBoxLayout()
        self.title = "Cadastro"
        self.top = 100
        self.left = 100
        self.width = 640
        self.height = 480
        self.setWindowIcon(QIcon("Icones/impressora.png"))
        self.setLayout(self.vbox)

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
                        AND nr_caixa = {0}""".format(str(self.nr_caixa))

        self.cursor.execute(comando_sql)
        dados_lidos = self.cursor.fetchall()
        y = 0
        pdf = canvas.Canvas("recibo.pdf")
        pdf.setFont("Times-Bold", 18)
        pdf.drawString(90, 800, "MINA & MINEKO ART. FAMELE:")
        pdf.setFont("Times-Bold", 12)

        pdf.drawString(10, 750, "ID")
        pdf.drawString(50, 750, "PRODUTO")
        pdf.drawString(260, 750, "QTD.")
        pdf.drawString(310, 750, "PREÇO UN.")
        pdf.drawString(390, 750, "SUB.TOTAL")
        pdf.drawString(470, 750, "TOTAL")
        pdf.drawString(3, 750,
                       "________________________________________________________________________________________")

        total = 0
        subtotal = 0
        for i in range(0, len(dados_lidos)):
            y += 50
            # CODIGO PRODUTO
            pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
            # DESCRIÇAO PRODUTO
            pdf.drawString(50, 750 - y, str(dados_lidos[i][1]))
            # QUANTIDADE VENDIDA
            pdf.drawString(260, 750 - y, str(dados_lidos[i][2]))
            # PREÇO UNITARIO
            pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
            subtotal = (dados_lidos[i][3]) * \
                dados_lidos[i][2]  # QTD x PREÇO UNITARIO
            total += subtotal
            pdf.drawString(390, 750 - y, str(subtotal))  # SUB TOTAL
        pdf.drawString(470, 750 - y, str(total))  # TOTAL

        pdf.save()

        with open('recibo.csv', 'w') as f:
            csv_writer = csv.writer(f)
            rows = [i for i in dados_lidos]
            csv_writer.writerows(rows)

        self.InitWindow()

    def InitWindow(self):
        '''Permie visualizar a impressão em tela, mas estva fechando a tela principal
        por isso eu desativei a chamada'''
        self.hbox = QHBoxLayout()

        self.print_btn = QPushButton("IMPRIMIR", self)
        self.print_btn.clicked.connect(self.print)

        self.view_btn = QPushButton("VISUALIZAR", self)
        self.view_btn.clicked.connect(self.view)

        self.rw = PrettyTable()
        self.rw.field_names = ["Cod.", "Descrição",
                               "Quant.", "Preco unit.", "Subtotal\n"]
        try:
            with open("recibo.csv", "r") as msg:
                self.lin = [x.strip().split(",") for x in msg]

                self.a = [self.lin[x] for x in range(len(self.lin))]

                total = 0
                for x in self.a:
                    self.rw.set_style(PLAIN_COLUMNS)
                    self.rw.add_row(x)

                for sub in range(len(self.a)):
                    total += float(self.a[sub][4])

                print(self.rw)
                msg.close()
        except Exception as e:
            self.errors(e)

        empresa = "MINA & MINEKO ART. FEMININS E TABACARIA"
        endereco = "Rua Enestina Loschi n.76"
        telefone = "(11) 97151-2237 / (11) 97561-8992)"
        text = f'\n\nTOTAL: {total:>130} \n\nEmpresa: {empresa:^90} \nEndereço: {endereco:^90} \nTelefones: {telefone:^90}'

        newGroup = QGroupBox("LISTA DE PRODUTOS")
        newGroup.setStyleSheet(
            f"background-color: {self.black}; color: {self.yellow}")

        self.edt = QTextEdit(self)
        self.edt.setAcceptRichText(True)
        self.edt.setReadOnly(True)
        self.edt.setText(f"{self.rw} \n{text}")
        self.vbox.addWidget(self.edt)

        self.hbox.addWidget(self.print_btn)
        # self.hbox.addWidget(self.view_btn)
        self.vbox.addLayout(self.hbox)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def errors(self, e):
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err = f"{e} \n{exc_type} \n{fname} \n{exc_tb.tb_lineno} \n"
        print(err)

    def print(self):
        prt = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(prt)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.edt.print_(prt)
            # self.hide()
            telaprincipal()
        # telaprincipal()

    def view(self):
        pt = QPrinter(QPrinter.HighResolution)
        prev = QPrintPreviewDialog(pt, self)
        prev.paintRequested.connect(self.preview)
        prev.exec_()

    def preview(self, pt):
        self.edt.print_(pt)

    # testar a criação de um arquivo csv baseado na table
    def export_to_csv(self, w):
        try:
            with open('recibo.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow((w.table.horizontalHeaderItem(
                    0).text(), w.table.horizontalHeaderItem(1).text()))
                for rowNumber in range(w.table.rowCount()):
                    writer.writerow(
                        [w.table.item(rowNumber, 0).text(), w.table.item(rowNumber, 1).text()])
                print('CSV file exported.')
            file.close()
        except Exception as e:
            print(e)
