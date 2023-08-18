from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QDoubleValidator, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)


class DecimalLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            if event.key() == 44:  # Código da tecla vírgula
                event = event.replace(44, 46)  # Substituir vírgula por ponto

            if not event.text().isnumeric() and event.text() != "." or ",":
                return True  # Ignorar eventos de teclado não numéricos

        return super().eventFilter(obj, event)


class AberturaCaixa(QDialog):
    """
    Define uma nova janela onde inserimos os valores de abertura do caixa do dia
    """

    def __init__(self, *args, **kwargs):
        super(AberturaCaixa, self).__init__(*args, **kwargs)

        # Restante do código permanece o mesmo

        self.caixainicio = DecimalLineEdit()
        self.onlyFloat = QDoubleValidator()
        self.caixainicio.setValidator(self.onlyFloat)
        self.caixainicio.setPlaceholderText("R$ Valor inicial")
        layout.addWidget(self.caixainicio)

        self.caixainicio.installEventFilter(self.caixainicio)

        self.caixainicio.installEventFilter(
            self.caixainicio
        )  # Instala o filtro de evento

        # Restante do código permanece o mesmo
