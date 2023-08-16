
def valoreAbertura(self):
    print(f'Entrou na função valoreAbertura')

    dataAtual = QDate.currentDate()
    data = dataAtual.toPyDate()
    valor_do_dia = []
    vendas_do_dia = []
    self.soma_fechamento = 0
    valor_inicial = 0
    valor_abertura = []

    self.cursor = conexao.banco.cursor()
        consulta_sql = (
            "SELECT valor FROM livro where status = '{}' and dataAtual = '{}';".format(
                "I", data
            )
        )
        self.cursor.execute(consulta_sql)
        self.valor_inicial = self.cursor.fetchall()

        for val in range(len(self.valor_inicial)):
            valor_inicial = float(self.valor_inicial[val][0])
            valor_abertura.append(valor_inicial)

        print("Mostra valores que iniciamos o caixa", valor_abertura)

def valorFechamento(self):
        print(f'Entrou na função valorFechamento')

        dataAtual = QDate.currentDate()
        data = dataAtual.toPyDate()        
        valor_do_dia = []
        vendas_do_dia = []
        self.soma_fechamento = 0
        valor_inicial = 0
        valor_abertura = []

        try:
            self.cursor = conexao.banco.cursor()
            consulta_sql_fechamento = "SELECT valorfechamento FROM livro where status = '{}' and dataAtual = '{}';".format(
                "F", data
            )
            self.cursor.execute(consulta_sql_fechamento)
            self.valor_fechamento = self.cursor.fetchall()
        except Exception as e:
            print("Sem valor de fechamento", e)

        valor_fechamento = 0
        for val in range(len(self.valor_fechamento)):
            valor_fechamento = float(self.valor_fechamento[val][0])

        abertura_X_fechamento = list(map(adicionar_imposto, precos))

        print(f"Valor de fechamento = {valor_fechamento}")



def relatorioFechamentocaixa(self):
        """Relatório de fechamento do Caixa"""

        dataAtual = QDate.currentDate()
        data = dataAtual.toPyDate()

        valor_do_dia = []
        vendas_do_dia = []
        self.soma_fechamento = 0
        valor_inicial = 0
        valor_abertura = []

        y = 0
        pdf = canvas.Canvas("fechamento_caixa.pdf")
        pdf.setFont("Times-Bold", 18)
        pdf.drawString(90, 800, "RELATÓRIO DE FECHAMENTO DO CAIXA:")
        pdf.setFont("Times-Bold", 12)

        valoreAbertura(self)
        valorFechamento(self)

        try:
            """Pega o valor total dos pedidos ate o ultimo fechamento na data atual"""

            self.cursor = conexao.banco.cursor()
            __fechamento = "SELECT ultupdate, valor_total, nr_caixa FROM pedidocaixa"
            self.cursor.execute(__fechamento)
            fechamento_diario = self.cursor.fetchall()

            self.cursor = conexao.banco.cursor()
            __fechamento_nr_caixa = """ SELECT nr_caixa, SUM(valor_total) as TOTAL
                                FROM controle_clientes.pedidocaixa
                                group by nr_caixa
                                order by nr_caixa desc
                                limit 0, 2 """
            self.cursor.execute(__fechamento_nr_caixa)
            self.fechamento_diario_nr_caixa = self.cursor.fetchall()

            # eu estou pegando na tabela pedidocaixa o valor do
            # campo nr_caixa que é gerado a cada vez que se fecha o
            # caixa para garantir que apenas os valores totais de compras
            #  de cada compra seja computado a cada fechamento.

            lista_numero_de_caixa = []
            data_fechamento1 = [fecha for fecha in self.fechamento_diario_nr_caixa]
            for dtnumber1 in range(len(data_fechamento1)):
                self.numero_caixa = data_fechamento1[dtnumber1][0]
                lista_numero_de_caixa.append(self.numero_caixa)

            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            self.numero_caixa_fechamento = int(lista_numero_de_caixa[0])
            print(">>>>>>>>>>>>>>", self.numero_caixa_fechamento)

            data_fechamento = [fecha for fecha in fechamento_diario]
            for dtnumber in range(len(data_fechamento)):
                if dataAtual == data_fechamento[dtnumber][0]:
                    # Pega o valor de cada pedido referente a data atual
                    # e insere na lista de valor do dia (pedidos vendido na data atual)
                    valor_do_dia.append(data_fechamento[dtnumber][1])
                    self.soma_fechamento += data_fechamento[dtnumber][1]
          

            # DATA DO FECHAMENTO
            pdf.drawString(10, 700 - y, str("{}").format(data_fechamento[dtnumber][0]))

            # VALOR DA ABERTURA

            # pdf.drawString(90, 700 - y, str({}).format(valor_inicial))

            pdf.drawString(10, 750, "Data")
            pdf.drawString(90, 750, "Nr.A")
            pdf.drawString(160, 750, "Abertura")
            pdf.drawString(220, 750, "Vendas")
            pdf.drawString(310, 750, "Abertura + Vendas.")
            pdf.drawString(440, 750, "Saldo Caixa.")
            pdf.drawString(
                3,
                750,
                "________________________________________________________________________________________",
            )

            total = 0
            subtotal = 0
            i = 0
            i = [i for i in valor_do_dia]
            cont = len(i)
            c = 0
            while cont > 0:
                total += float(i[c])
                cont -= 1
                c += 1

            total_abertura = 0
            i_valorAbertura = [i for i in valor_abertura]

            contador = len(i_valorAbertura)
            ct = 0
            while contador > 0:
                caixa_iniciado = i_valorAbertura[ct]
                # total_abertura += i_valorAbertura[ct]

                pdf.drawString(
                    90,
                    700 - y,
                    str({}).format(self.numero_caixa_fechamento),  # numero da abertura
                )
                pdf.drawString(
                    160, 700 - y, str({}).format(caixa_iniciado)
                )  # Valor da abertura
                # pdf.drawString(220, 700 - y, str(total))
                # pdf.drawString(310, 700 - y, str(valor_fechamento))
                pdf.drawString(
                    440, 700 - y, str(float(valor_fechamento) - float(subtotal))
                )
                contador -= 1
                ct += 1
                y += 50
            # pdf.drawString(220, 700 - y, str(total))

            pdf.save()
            valor_do_dia = []

        except Exception as e:
            print(e)