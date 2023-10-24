import os
from datetime import datetime

import mysql.connector

# Importe as informações de conexão do arquivo conexão.py
import conexao


def backup_database():
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

                print(f"Backup concluído em {backup_file}")

            except Exception as e:
                print(f"Erro ao fazer o backup - {str(e)}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    backup_database()
