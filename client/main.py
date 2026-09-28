import sys
from PySide6.QtWidgets import QApplication, QMessageBox

from client.api_client import APIClient
from client.styles import DARK_THEME  # Импорт темы
from client.views import EmployeeDashboard, LoginWindow, ManagerDashboard


class ApplicationManager:

    def __init__(self):
        self.app = QApplication(sys.argv)

        # Применяем единый стиль оформление на уровень приложения
        self.app.setStyleSheet(DARK_THEME)

        self.api_client = APIClient()

        # Создаем и настраиваем окно логина
        self.login_window = LoginWindow(self.api_client)
        self.login_window.login_success.connect(self.on_login_success)

        self.main_window = None

    def run(self):
        self.login_window.show()
        sys.exit(self.app.exec())

    def on_login_success(self):
        self.login_window.close()

        # Запрашиваем информацию о текущем пользователе для определения роли
        user_info = self.api_client.get_current_user_info()

        if not user_info:
            QMessageBox.critical(
                None, "Ошибка", "Не удалось получить профиль пользователя."
            )
            return

        role = user_info.get("role")

        # Открываем нужный интерфейс в зависимости от роли
        if role == "MANAGER" or user_info.get("is_superuser"):
            self.main_window = ManagerDashboard(self.api_client)
        else:
            self.main_window = EmployeeDashboard(self.api_client)

        self.main_window.show()


def main():
    app_manager = ApplicationManager()
    app_manager.run()


if __name__ == "__main__":
    main()