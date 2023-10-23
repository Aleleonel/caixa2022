import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ConfiguracaoSistemaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Configurações do Sistema")
        self.setGeometry(100, 100, 400, 200)

        self.label_empresa = QLabel("Nome da Empresa:")
        self.empresa_input = QLineEdit(self)
        self.label_diretorio_arquivos = QLabel("Diretório de Salvamento de Arquivos:")
        self.diretorio_arquivos_input = QLineEdit(self)
        self.label_diretorio_backup = QLabel("Diretório de Backup do Banco de Dados:")
        self.diretorio_backup_input = QLineEdit(self)
        self.btn_salvar = QPushButton("Salvar", self)
        self.btn_salvar.clicked.connect(self.salvar_configuracoes)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_empresa)
        self.layout.addWidget(self.empresa_input)
        self.layout.addWidget(self.label_diretorio_arquivos)
        self.layout.addWidget(self.diretorio_arquivos_input)
        self.layout.addWidget(self.label_diretorio_backup)
        self.layout.addWidget(self.diretorio_backup_input)
        self.layout.addWidget(self.btn_salvar)

        self.setLayout(self.layout)

    def salvar_configuracoes(self):
        nome_empresa = self.empresa_input.text()
        diretorio_arquivos = self.diretorio_arquivos_input.text()
        diretorio_backup = self.diretorio_backup_input.text()

        # Aqui, você pode salvar as configurações em algum lugar, como um arquivo de configuração
        # ou em um banco de dados.

        print(f"Nome da Empresa: {nome_empresa}")
        print(f"Diretório de Salvamento de Arquivos: {diretorio_arquivos}")
        print(f"Diretório de Backup do Banco de Dados: {diretorio_backup}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConfiguracaoSistemaApp()
    ex.show()
    sys.exit(app.exec_())
