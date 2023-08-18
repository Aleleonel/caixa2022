import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)


class NumericLineEdit(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Digite um valor numérico:")
        self.line_edit = QLineEdit()
        self.line_edit.setAlignment(Qt.AlignRight)

        self.line_edit.textChanged.connect(self.validate_input)

        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

    def validate_input(self):
        text = self.line_edit.text()

        if not text:
            return

        try:
            float(text)
            self.line_edit.setStyleSheet("")
        except ValueError:
            self.line_edit.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(
                self, "Valor Inválido", "Digite um valor numérico válido."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumericLineEdit()
    window.setWindowTitle("Validação Numérica")
    window.show()
    sys.exit(app.exec_())
