import os
import shutil
import sys

import mysql.connector
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Importe as informações de conexão do arquivo conexão.py
import conexao


class DatabaseBackupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Backup do Banco de Dados MySQL")
        self.setGeometry(100, 100, 400, 150)

        self.backup_button = QPushButton("Realizar Backup")
        self.backup_button.clicked.connect(self.backup_database)

        self.label = QLabel("Status: Aguardando Backup")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.backup_button)
        self.setLayout(layout)

    def backup_database(self):
        try:
            # Use as informações de conexão do arquivo conexão.py
            connection = conexao.banco

            if connection.is_connected():
                cursor = connection.cursor()

                try:
                    # Defina o diretório de destino do backup
                    backup_directory = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)), "backup"
                    )

                    # Crie o diretório de backup, se não existir
                    if not os.path.exists(backup_directory):
                        os.makedirs(backup_directory)

                    # Nomeie o arquivo de backup com a data e hora atual
                    backup_file = os.path.join(
                        backup_directory,
                        f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql",
                    )

                    # Use o utilitário mysqldump para fazer o backup do banco de dados
                    backup_config = {
                        "user": connection.user,
                        "passwd": connection._password,
                        "host": connection._host,
                        "database": connection.database,
                    }
                    mysqldump_cmd = f"mysqldump -u {backup_config['user']} -p{backup_config['passwd']} -h {backup_config['host']} {backup_config['database']} > {backup_file}"
                    os.system(mysqldump_cmd)

                    self.label.setText(f"Status: Backup concluído em {backup_file}")
                    QMessageBox.information(
                        self,
                        "Backup Concluído",
                        "O backup foi concluído com sucesso!",
                    )

                except Exception as e:
                    self.label.setText(f"Status: Erro ao fazer o backup - {str(e)}")
                    QMessageBox.critical(
                        self,
                        "Erro de Backup",
                        f"Ocorreu um erro ao fazer o backup: {str(e)}",
                    )

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    from datetime import datetime

    app = QApplication(sys.argv)
    window = DatabaseBackupApp()
    window.show()
    sys.exit(app.exec_())