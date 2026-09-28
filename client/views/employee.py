from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class TaskCard(QFrame):
    """Карточка задачи для сотрудника"""

    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task_id = task.get("id")
        self.status_raw = str(task.get("status", "NEW")).upper()
        self.is_selected = False

        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("taskCard")

        # Основной макет карточки
        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(12)

        # 1. Верхняя строка: Заголовок и бейдж статуса
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        title_label = QLabel(str(task.get("title", "Без названия")))
        title_label.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: 700; color: #f1f5f9; border: none; background: transparent; }"
        )
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, stretch=1)

        # Оформление статуса
        status_info = {
            "NEW": ("● Новая", "#60a5fa", "rgba(96, 165, 250, 0.12)"),
            "IN_PROGRESS": ("⚡ В работе", "#fbbf24", "rgba(251, 191, 36, 0.12)"),
            "COMPLETED": ("✓ Завершено", "#34d399", "rgba(52, 211, 153, 0.12)"),
        }
        st_text, st_color, st_bg = status_info.get(
            self.status_raw, (self.status_raw, "#94a3b8", "rgba(148, 163, 184, 0.12)")
        )

        status_badge = QLabel(st_text)
        status_badge.setStyleSheet(
            f"QLabel {{"
            f"   color: {st_color};"
            f"   background-color: {st_bg};"
            f"   font-size: 12px;"
            f"   font-weight: 600;"
            f"   padding: 4px 10px;"
            f"   border-radius: 6px;"
            f"   border: none;"
            f"}}"
        )
        header_layout.addWidget(status_badge, alignment=Qt.AlignmentFlag.AlignTop)

        card_layout.addLayout(header_layout)

        # 2. Описание задачи
        desc_text = task.get("description", "").strip()
        if desc_text:
            desc_container = QFrame()
            desc_container.setStyleSheet(
                "QFrame {"
                "   background-color: #0b0f17;"
                "   border: 1px solid #1e293b;"
                "   border-radius: 8px;"
                "}"
            )
            desc_layout = QVBoxLayout(desc_container)
            desc_layout.setContentsMargins(14, 12, 14, 12)

            desc_label = QLabel(desc_text)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet(
                "QLabel {"
                "   color: #cbd5e1;"
                "   font-size: 13px;"
                "   line-height: 1.5;"
                "   font-family: 'Consolas', 'Courier New', monospace;"
                "   border: none;"
                "   background: transparent;"
                "}"
            )
            desc_layout.addWidget(desc_label)
            card_layout.addWidget(desc_container)

        # 3. Нижняя строка: ID задачи
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 4, 0, 0)
        footer_layout.addStretch(1)

        id_label = QLabel(f"#{self.task_id}")
        id_label.setStyleSheet(
            "QLabel { color: #475569; font-size: 12px; font-weight: 600; border: none; background: transparent; }"
        )
        footer_layout.addWidget(id_label)

        card_layout.addLayout(footer_layout)

        self.update_style()

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.update_style()

    def update_style(self):
        if self.is_selected:
            self.setStyleSheet(
                "QFrame#taskCard {"
                "   background-color: #162032;"
                "   border: 2px solid #6366f1;"
                "   border-radius: 12px;"
                "}"
            )
        else:
            self.setStyleSheet(
                "QFrame#taskCard {"
                "   background-color: #111827;"
                "   border: 1px solid #1f293d;"
                "   border-radius: 12px;"
                "}"
                "QFrame#taskCard:hover {"
                "   border: 1px solid #3b82f6;"
                "   background-color: #162032;"
                "}"
            )


class EmployeeDashboard(QWidget):

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.selected_card = None

        self.setWindowTitle("Рабочая панель — Сотрудник")
        self.resize(950, 750)

        # Главный стиль приложения
        self.setStyleSheet(
            "QWidget {"
            "   background-color: #0b0f17;"
            "   color: #e2e8f0;"
            "   font-family: 'Inter', 'Segoe UI', sans-serif;"
            "}"
            "QScrollArea {"
            "   border: none;"
            "   background-color: transparent;"
            "}"
            "QScrollBar:vertical {"
            "   background: #0b0f17;"
            "   width: 8px;"
            "   border-radius: 4px;"
            "}"
            "QScrollBar::handle:vertical {"
            "   background: #1f293d;"
            "   border-radius: 4px;"
            "}"
            "QScrollBar::handle:vertical:hover {"
            "   background: #334155;"
            "}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        # --- 1. Карточка профиля ---
        profile_card = QFrame()
        profile_card.setStyleSheet(
            "QFrame {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   border-radius: 14px;"
            "}"
        )

        profile_layout = QVBoxLayout(profile_card)
        profile_layout.setContentsMargins(20, 20, 20, 20)
        profile_layout.setSpacing(6)
        profile_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.avatar_label = QLabel("E")
        self.avatar_label.setFixedSize(52, 52)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setStyleSheet(
            "QLabel {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #a855f7);"
            "   color: #ffffff;"
            "   font-size: 22px;"
            "   font-weight: 800;"
            "   border-radius: 26px;"
            "   border: none;"
            "}"
        )
        profile_layout.addWidget(
            self.avatar_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.user_name_label = QLabel("Загрузка...")
        self.user_name_label.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: 700; color: #ffffff; border: none; background: transparent; }"
        )
        self.user_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_layout.addWidget(self.user_name_label)

        self.user_role_label = QLabel("Сотрудник")
        self.user_role_label.setStyleSheet(
            "QLabel { font-size: 13px; color: #64748b; font-weight: 500; border: none; background: transparent; }"
        )
        self.user_role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_layout.addWidget(self.user_role_label)

        layout.addWidget(profile_card)

        # --- 2. Заголовок раздела задач ---
        self.label_heading = QLabel("Мои текущие задачи")
        self.label_heading.setStyleSheet(
            "QLabel { font-size: 20px; font-weight: 800; color: #ffffff; border: none; background: transparent; }"
        )
        layout.addWidget(self.label_heading)

        # --- 3. Область с прокруткой для карточек ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background-color: transparent;")
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(14)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.cards_container)
        layout.addWidget(self.scroll_area)

        # --- 4. Панель кнопок взаимодействия ---
        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)

        self.btn_in_progress = QPushButton("⚡ Взять в работу")
        self.btn_in_progress.setCursor(Qt.PointingHandCursor)
        self.btn_in_progress.setFixedHeight(44)
        self.btn_in_progress.setStyleSheet(
            "QPushButton {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #2563eb);"
            "   color: #ffffff;"
            "   border: none;"
            "   border-radius: 10px;"
            "   font-size: 14px;"
            "   font-weight: 700;"
            "}"
            "QPushButton:hover {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #1d4ed8);"
            "}"
            "QPushButton:disabled {"
            "   background-color: #1e293b;"
            "   color: #475569;"
            "}"
        )
        self.btn_in_progress.setEnabled(False)
        self.btn_in_progress.clicked.connect(self.on_click_in_progress)
        action_layout.addWidget(self.btn_in_progress)

        self.btn_complete = QPushButton("✓ Завершить")
        self.btn_complete.setCursor(Qt.PointingHandCursor)
        self.btn_complete.setFixedHeight(44)
        self.btn_complete.setStyleSheet(
            "QPushButton {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);"
            "   color: #ffffff;"
            "   border: none;"
            "   border-radius: 10px;"
            "   font-size: 14px;"
            "   font-weight: 700;"
            "}"
            "QPushButton:hover {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #047857);"
            "}"
            "QPushButton:disabled {"
            "   background-color: #1e293b;"
            "   color: #475569;"
            "}"
        )
        self.btn_complete.setEnabled(False)
        self.btn_complete.clicked.connect(self.on_click_complete)
        action_layout.addWidget(self.btn_complete)

        self.btn_refresh = QPushButton("🔄 Обновить список")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.setFixedHeight(44)
        self.btn_refresh.setStyleSheet(
            "QPushButton {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   color: #f8fafc;"
            "   border-radius: 10px;"
            "   font-size: 14px;"
            "   font-weight: 600;"
            "}"
            "QPushButton:hover {"
            "   background-color: #162032;"
            "   border: 1px solid #3b82f6;"
            "}"
        )
        self.btn_refresh.clicked.connect(self.load_my_tasks)
        action_layout.addWidget(self.btn_refresh)

        layout.addLayout(action_layout)

        self.load_profile_info()
        self.load_my_tasks()

    def load_profile_info(self):
        user = self.api_client.get_current_user_info()
        if user:
            first_name = user.get("first_name", "")
            last_name = user.get("last_name", "")
            username = user.get("username", "Сотрудник")

            if first_name or last_name:
                display_name = f"{first_name} {last_name}".strip()
            else:
                display_name = username

            initial = display_name[0].upper() if display_name else "E"

            self.user_name_label.setText(display_name)
            self.avatar_label.setText(initial)

    def load_my_tasks(self):
        # Очищаем старые карточки из контейнера
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.selected_card = None
        self.btn_in_progress.setEnabled(False)
        self.btn_complete.setEnabled(False)

        tasks = self.api_client.get_tasks()

        if not tasks:
            empty_label = QLabel("У вас пока нет назначенных задач")
            empty_label.setStyleSheet("color: #64748b; font-size: 14px; padding: 20px; border: none; background: transparent;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cards_layout.addWidget(empty_label)
            return

        for task in tasks:
            card = TaskCard(task)
            # Привязываем клик по карточке
            card.mousePressEvent = lambda event, c=card: self.select_card(c)
            self.cards_layout.addWidget(card)

    def select_card(self, card: TaskCard):
        # Снимаем выделение со старой карточки
        if self.selected_card:
            self.selected_card.set_selected(False)

        self.selected_card = card
        self.selected_card.set_selected(True)

        # Активируем кнопки в зависимости от статуса задачи в карточке
        status = card.status_raw
        if status == "NEW":
            self.btn_in_progress.setEnabled(True)
            self.btn_complete.setEnabled(False)
        elif status == "IN_PROGRESS":
            self.btn_in_progress.setEnabled(False)
            self.btn_complete.setEnabled(True)
        else:
            self.btn_in_progress.setEnabled(False)
            self.btn_complete.setEnabled(False)

    def on_click_in_progress(self):
        self.update_selected_task_status("IN_PROGRESS")

    def on_click_complete(self):
        self.update_selected_task_status("COMPLETED")

    def update_selected_task_status(self, new_status):
        if not self.selected_card:
            QMessageBox.warning(self, "Предупреждение", "Выберите карточку задачи.")
            return

        task_id = self.selected_card.task_id

        # Пробуем передать верхний регистр, если нет — нижний
        success = self.api_client.update_task_status(task_id, new_status)
        if not success:
            success = self.api_client.update_task_status(task_id, new_status.lower())

        if success:
            self.load_my_tasks()
        else:
            QMessageBox.critical(
                self, "Ошибка", "Не удалось обновить статус задачи на сервере."
            )