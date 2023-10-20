import subprocess
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ScriptRunnerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Executar Script Python")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText("Digite seu código Python aqui...")

        self.run_button = QPushButton("Executar", self)
        self.run_button.clicked.connect(self.run_script)

        self.open_button = QPushButton("Abrir Arquivo", self)
        self.open_button.clicked.connect(self.open_file)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.open_button)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Arquivo Python",
            "",
            "Python Files (*.py);;All Files (*)",
            options=options,
        )

        if file_name:
            with open(file_name, "r") as file:
                script_contents = file.read()
                self.text_edit.setPlainText(script_contents)

    def run_script(self):
        script_contents = self.text_edit.toPlainText()
        try:
            exec(script_contents)
        except Exception as e:
            self.text_edit.setPlainText(f"Erro ao executar o script:\n\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScriptRunnerApp()
    window.show()
    sys.exit(app.exec_())
