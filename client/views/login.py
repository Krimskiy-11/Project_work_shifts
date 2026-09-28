from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginWindow(QWidget):
    # Сигнал отправляется при успешной проверке логина и пароля
    login_success = Signal()

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Авторизация — Work Shifts")
        self.resize(350, 220)

        layout = QVBoxLayout()

        self.label_title = QLabel("Вход в систему")
        self.label_title.setStyleSheet(
            "font-size: 16px; font-weight: bold; margin-bottom: 10px;"
        )
        layout.addWidget(self.label_title)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Имя пользователя")
        layout.addWidget(self.input_username)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Пароль")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password)

        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.handle_login)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def handle_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QMessageBox.warning(
                self, "Ошибка", "Введите имя пользователя и пароль."
            )
            return

        if self.api_client.login(username, password):
            self.login_success.emit()
        else:
            QMessageBox.critical(
                self,
                "Ошибка входа",
                "Неверные учётные данные или сервер недоступен.",
            )