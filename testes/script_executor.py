import os
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class ScriptExecutorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Script Executor")
        self.setGeometry(100, 100, 600, 400)

        self.script_output = QTextBrowser(self)
        self.script_output.setGeometry(10, 10, 580, 200)

        self.select_script_button = QPushButton("Selecionar Script", self)
        self.select_script_button.setGeometry(10, 220, 150, 30)
        self.select_script_button.clicked.connect(self.select_script)

        self.run_script_button = QPushButton("Executar Script", self)
        self.run_script_button.setGeometry(170, 220, 150, 30)
        self.run_script_button.clicked.connect(self.run_script)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.script_output)
        self.layout.addWidget(self.select_script_button)
        self.layout.addWidget(self.run_script_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.selected_script_path = ""

    def select_script(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        self.selected_script_path, _ = file_dialog.getOpenFileName(
            self,
            "Selecionar Script",
            "",
            "Scripts (*.sh *.py);;Todos os Arquivos (*)",
            options=options,
        )

    def run_script(self):
        if not self.selected_script_path:
            self.script_output.append("Nenhum script selecionado.")
            return

        try:
            script_output = os.popen(f"bash {self.selected_script_path}").read()
            self.script_output.append(script_output)
        except Exception as e:
            self.script_output.append(f"Erro ao executar o script: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScriptExecutorApp()
    window.show()
    sys.exit(app.exec_())
