self.butonAbrirCaixa.clicked.connect(self.abrircaixa)

def statuscaixa(self):
        try:
            # varrer a tabela livro para pegar o valorcaixainiciado
            self.cursor = conexao.banco.cursor()
            consulta_sql = "SELECT status FROM livro ORDER BY idlivro DESC limit 1;"
            self.cursor.execute(consulta_sql)
            self.status_final = self.cursor.fetchall()

            self.status_finalizado = [
                resultado for resultado in self.status_final]
            for indice_final in range(len(self.status_finalizado)):
                      self.status_finalizado[indice_final][0]

            aberto = self.status_finalizado[indice_final][0]

            if aberto == "I":
                self.butonAbrirCaixa.setEnabled(False)

            elif aberto == "F":
                self.butonFecharCaixa.setEnabled(False)

            else:
                self.butonFecharCaixa.setEnabled(True)
                self.butonAbrirCaixa.setEnabled(False)
                replay = QMessageBox.question(self, 'Window close', 'Deseja realmente Fechar o caixa?',
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if replay == QMessageBox.Yes:

                    dataAtual = QDate.currentDate()
                    self.soma_fechamento = 0
                    valor_do_dia = []
                    decimal_lista = []
                    self.status = 'F'
                    dlg = FechamentoCaixa()
                    dlg.exec()
                else:
                    pass

        except (RuntimeError, TypeError, NameError):
            print('RuntimeError', str(RuntimeError))
            print('TypeError', str(TypeError))
            print('NameError', str(NameError))
