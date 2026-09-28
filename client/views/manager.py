from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class EditTaskDialog(QDialog):
    """Модальное окно для редактирования задачи менеджером (CRUD - Update)."""

    def __init__(self, task, users, parent=None):
        super().__init__(parent)
        self.task = task
        self.users = users

        self.setWindowTitle(f"Редактирование задачи #{task.get('id')}")
        self.setFixedSize(460, 480)
        self.setStyleSheet(
            "QDialog {"
            "   background-color: #0b0f17;"
            "   color: #e2e8f0;"
            "   font-family: 'Inter', 'Segoe UI', sans-serif;"
            "}"
            "QLineEdit, QTextEdit, QComboBox, QDateEdit {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   border-radius: 8px;"
            "   padding: 8px 12px;"
            "   color: #f8fafc;"
            "   font-size: 13.5px;"
            "}"
            "QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {"
            "   border: 1px solid #6366f1;"
            "}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title_lbl = QLabel("Редактировать задачу")
        title_lbl.setStyleSheet(
            "font-size: 18px; font-weight: 800; color: #ffffff; border: none; background: transparent;"
        )
        layout.addWidget(title_lbl)

        form = QVBoxLayout()
        form.setSpacing(10)

        # Название
        form.addWidget(
            QLabel("Название:",
                styleSheet="color: #94a3b8; font-size: 12px; font-weight: 600; border: none; background: transparent;",
            )
        )
        self.input_title = QLineEdit(str(task.get("title", "")))
        form.addWidget(self.input_title)

        # Описание
        form.addWidget(
            QLabel(
                "Описание:",
                styleSheet="color: #94a3b8; font-size: 12px; font-weight: 600; border: none; background: transparent;",
            )
        )
        self.input_description = QTextEdit()
        self.input_description.setPlainText(str(task.get("description", "")))
        self.input_description.setMaximumHeight(90)
        form.addWidget(self.input_description)

        # Исполнитель
        form.addWidget(
            QLabel(
                "Исполнитель:",
                styleSheet="color: #94a3b8; font-size: 12px; font-weight: 600; border: none; background: transparent;",
            )
        )
        self.combo_assigned = QComboBox()

        current_assigned_id = task.get("assigned_to")
        if isinstance(current_assigned_id, dict):
            current_assigned_id = current_assigned_id.get("id")

        for user in self.users:
            uname = user.get("username", "")
            fname = user.get("first_name", "")
            lname = user.get("last_name", "")
            disp = f"{fname} {lname} (@{uname})".strip() if fname or lname else uname
            self.combo_assigned.addItem(disp, userData=user.get("id"))

            if user.get("id") == current_assigned_id:
                self.combo_assigned.setCurrentIndex(self.combo_assigned.count() - 1)

        form.addWidget(self.combo_assigned)

        # Срок выполнения (due_date)
        form.addWidget(
            QLabel(
                "Срок выполнения:",
                styleSheet="color: #94a3b8; font-size: 12px; font-weight: 600; border: none; background: transparent;",
            )
        )
        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)

        raw_due_date = task.get("due_date")
        if raw_due_date:
            parsed_date = QDate.fromString(raw_due_date[:10], "yyyy-MM-dd")
            self.date_picker.setDate(
                parsed_date if parsed_date.isValid() else QDate.currentDate()
            )
        else:
            self.date_picker.setDate(QDate.currentDate().addDays(3))

        form.addWidget(self.date_picker)

        layout.addLayout(form)

        # Кнопки отмены и сохранения
        btn_box = QHBoxLayout()
        btn_box.setSpacing(10)

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setFixedHeight(38)
        self.btn_save.setStyleSheet(
            "QPushButton {"
            "   background-color: #6366f1;"
            "   color: #ffffff;"
            "   border: none;"
            "   border-radius: 8px;"
            "   font-weight: 700;"
            "}"
            "QPushButton:hover { background-color: #4f46e5; }"
        )
        self.btn_save.clicked.connect(self.accept)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setFixedHeight(38)
        self.btn_cancel.setStyleSheet(
            "QPushButton {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   color: #94a3b8;"
            "   border-radius: 8px;"
            "   font-weight: 600;"
            "}"
            "QPushButton:hover { background-color: #162032; color: #f8fafc; }"
        )
        self.btn_cancel.clicked.connect(self.reject)

        btn_box.addWidget(self.btn_cancel)
        btn_box.addWidget(self.btn_save)

        layout.addLayout(btn_box)

    def get_data(self):
        return {
            "title": self.input_title.text().strip(),
            "description": self.input_description.toPlainText().strip(),
            "assigned_to": self.combo_assigned.currentData(),
            "due_date": self.date_picker.date().toString("yyyy-MM-dd"),
        }


class EmployeeCard(QFrame):
    """Карточка сотрудника."""

    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "EmployeeCard {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   border-radius: 12px;"
            "}"
            "EmployeeCard:hover {"
            "   border: 1px solid #6366f1;"
            "   background-color: #162032;"
            "}"
        )

        card_layout = QHBoxLayout(self)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(16)

        name = user.get("first_name") or user.get("username", "U")
        first_letter = name[0].upper() if name else "U"

        avatar_label = QLabel(first_letter)
        avatar_label.setFixedSize(44, 44)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_label.setStyleSheet(
            "QLabel {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #a855f7);"
            "   color: #ffffff;"
            "   font-size: 18px;"
            "   font-weight: 700;"
            "   border-radius: 22px;"
            "   border: none;"
            "}"
        )
        card_layout.addWidget(avatar_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        top_line = QHBoxLayout()
        top_line.setSpacing(10)

        full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        if not full_name:
            full_name = user.get("username", "Сотрудник")

        name_label = QLabel(full_name)
        name_label.setStyleSheet(
            "QLabel { color: #f8fafc; font-size: 15px; font-weight: 700; border: none; background: transparent; }"
        )
        top_line.addWidget(name_label)

        dept_info = user.get("department_detail") or {}
        dept_name = dept_info.get("name") or "Без отдела"

        dept_badge = QLabel(f"🏢 {dept_name}")
        dept_badge.setStyleSheet(
            "QLabel {"
            "   color: #c084fc;"
            "   background-color: rgba(192, 132, 252, 0.12);"
            "   font-size: 11px;"
            "   font-weight: 600;"
            "   padding: 3px 8px;"
            "   border-radius: 6px;"
            "   border: none;"
            "}"
        )
        top_line.addWidget(dept_badge)
        top_line.addStretch(1)

        info_layout.addLayout(top_line)

        sub_line = QHBoxLayout()
        sub_line.setSpacing(16)

        username = user.get("username", "")
        if username:
            uname_label = QLabel(f"@{username}")
            uname_label.setStyleSheet(
                "QLabel { color: #818cf8; font-size: 13px; font-weight: 500; border: none; background: transparent; }"
            )
            sub_line.addWidget(uname_label)

        email = user.get("email", "")
        if email:
            email_label = QLabel(f"✉ {email}")
            email_label.setStyleSheet(
                "QLabel { color: #64748b; font-size: 13px; border: none; background: transparent; }"
            )
            sub_line.addWidget(email_label)

        sub_line.addStretch(1)
        info_layout.addLayout(sub_line)

        card_layout.addLayout(info_layout, stretch=1)


class ManagerTaskCard(QFrame):
    """Карточка задачи с кнопками редактирования и удаления."""

    def __init__(self, task, on_edit_callback, on_delete_callback, parent=None):
        super().__init__(parent)
        self.task = task
        self.task_id = task.get("id")
        self.status_raw = str(task.get("status", "NEW")).upper()
        self.on_edit_callback = on_edit_callback
        self.on_delete_callback = on_delete_callback

        self.setStyleSheet(
            "ManagerTaskCard {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   border-radius: 12px;"
            "}"
            "ManagerTaskCard:hover {"
            "   border: 1px solid #3b82f6;"
            "   background-color: #162032;"
            "}"
        )

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(12)

        # 1. Заголовок и статус
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        title_label = QLabel(str(task.get("title", "Без названия")))
        title_label.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: 700; color: #f1f5f9; border: none; background: transparent; }"
        )
        header_layout.addWidget(title_label, stretch=1)

        status_config = {
            "NEW": ("● Новая", "#60a5fa", "rgba(96, 165, 250, 0.12)"),
            "IN_PROGRESS": ("⚡ В работе", "#fbbf24", "rgba(251, 191, 36, 0.12)"),
            "COMPLETED": ("✓ Завершено", "#34d399", "rgba(52, 211, 153, 0.12)"),
            "CANCELED": ("✕ Отменена", "#f87171", "rgba(248, 113, 113, 0.12)"),
        }
        st_text, st_color, st_bg = status_config.get(
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
        header_layout.addWidget(status_badge)
        card_layout.addLayout(header_layout)

        # 2. Описание
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

        # 3. Подвал: Исполнитель, Кнопки управления и ID
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 4, 0, 0)
        footer_layout.setSpacing(10)

        assigned_detail = task.get("assigned_to_detail") or {}
        employee_name = assigned_detail.get(
            "username", str(task.get("assigned_to", "—"))
        )

        emp_label = QLabel(
            f"👤 Исполнитель:  <b style='color: #e2e8f0;'>{employee_name}</b>"
        )
        emp_label.setStyleSheet(
            "QLabel { color: #64748b; font-size: 13px; border: none; background: transparent; }"
        )
        footer_layout.addWidget(emp_label)

        due_date = task.get("due_date")
        if due_date:
            due_label = QLabel(f"📅 До: {due_date[:10]}")
            due_label.setStyleSheet(
                "QLabel { color: #f59e0b; font-size: 12px; font-weight: 600; border: none; background: transparent; }"
            )
            footer_layout.addWidget(due_label)

        footer_layout.addStretch(1)

        # Кнопка "Редактировать"
        btn_edit = QPushButton("✏️")
        btn_edit.setToolTip("Редактировать задачу (Update)")
        btn_edit.setCursor(Qt.PointingHandCursor)
        btn_edit.setFixedSize(30, 30)
        btn_edit.setStyleSheet(
            "QPushButton {"
            "   background-color: #1e293b;"
            "   border: 1px solid #334155;"
            "   border-radius: 6px;"
            "   font-size: 12px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #3b82f6;"
            "   border: none;"
            "}"
        )
        btn_edit.clicked.connect(lambda: self.on_edit_callback(self.task))
        footer_layout.addWidget(btn_edit)

        # Кнопка "Удалить"
        btn_delete = QPushButton("🗑️")
        btn_delete.setToolTip("Удалить задачу (Delete)")
        btn_delete.setCursor(Qt.PointingHandCursor)
        btn_delete.setFixedSize(30, 30)
        btn_delete.setStyleSheet(
            "QPushButton {"
            "   background-color: #1e293b;"
            "   border: 1px solid #334155;"
            "   border-radius: 6px;"
            "   font-size: 12px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #ef4444;"
            "   border: none;"
            "}"
        )
        btn_delete.clicked.connect(lambda: self.on_delete_callback(self.task_id))
        footer_layout.addWidget(btn_delete)

        id_label = QLabel(f"#{self.task_id}")
        id_label.setStyleSheet(
            "QLabel { color: #475569; font-size: 12px; font-weight: 600; border: none; background: transparent; }"
        )
        footer_layout.addWidget(id_label)

        card_layout.addLayout(footer_layout)


class ManagerDashboard(QWidget):

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.all_users = []
        self.setWindowTitle("Панель управления — Менеджер")
        self.resize(1100, 720)

        self.setStyleSheet(
            "QWidget {"
            "   background-color: #0b0f17;"
            "   color: #e2e8f0;"
            "   font-family: 'Inter', 'Segoe UI', sans-serif;"
            "}"
            "QLineEdit, QTextEdit, QDateEdit {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   border-radius: 10px;"
            "   padding: 10px 14px;"
            "   color: #f8fafc;"
            "   font-size: 14px;"
            "}"
            "QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {"
            "   border: 1px solid #6366f1;"
            "   background-color: #161f33;"
            "}"
            "QComboBox {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   border-radius: 10px;"
            "   padding: 10px 14px;"
            "   color: #f8fafc;"
            "   font-size: 14px;"
            "}"
            "QComboBox:focus {"
            "   border: 1px solid #6366f1;"
            "}"
            "QComboBox::drop-down {"
            "   border: none;"
            "   padding-right: 12px;"
            "}"
            "QComboBox QAbstractItemView {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   selection-background-color: #6366f1;"
            "   color: #ffffff;"
            "   outline: none;"
            "}"
            "QScrollArea {"
            "   border: none;"
            "   background-color: transparent;"
            "}"
        )

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Боковая панель
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet(
            "QFrame {"
            "   background-color: #0d131f;"
            "   border-right: 1px solid #1e293b;"
            "}"
        )

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 24, 18, 24)
        sidebar_layout.setSpacing(20)

        profile_box = QHBoxLayout()
        profile_box.setSpacing(12)

        self.avatar_label = QLabel("M")
        self.avatar_label.setStyleSheet(
            "QLabel {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #a855f7);"
            "   color: #ffffff;"
            "   font-size: 16px;"
            "   font-weight: 800;"
            "   border-radius: 20px;"
            "   min-width: 40px; max-width: 40px;"
            "   min-height: 40px; max-height: 40px;"
            "   border: none;"
            "}"
        )
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_box.addWidget(self.avatar_label)

        profile_info = QVBoxLayout()
        profile_info.setSpacing(2)

        self.user_name_label = QLabel("Загрузка...")
        self.user_name_label.setStyleSheet(
            "QLabel { font-size: 14px; font-weight: 700; color: #ffffff; border: none; background: transparent; }"
        )
        profile_info.addWidget(self.user_name_label)

        self.user_role_label = QLabel("Менеджер")
        self.user_role_label.setStyleSheet(
            "QLabel { font-size: 12px; color: #64748b; font-weight: 500; border: none; background: transparent; }"
        )
        profile_info.addWidget(self.user_role_label)

        profile_box.addLayout(profile_info)
        sidebar_layout.addLayout(profile_box)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet(
            "background-color: #1e293b; max-height: 1px; border: none;"
        )
        sidebar_layout.addWidget(divider)

        self.btn_nav_create = self.create_nav_button("➕   Создать задачу")
        self.btn_nav_create.clicked.connect(lambda: self.switch_tab(0))
        sidebar_layout.addWidget(self.btn_nav_create)

        self.btn_nav_tasks = self.create_nav_button("📋   Список задач")
        self.btn_nav_tasks.clicked.connect(lambda: self.switch_tab(1))
        sidebar_layout.addWidget(self.btn_nav_tasks)

        self.btn_nav_employees = self.create_nav_button("👥   Сотрудники")
        self.btn_nav_employees.clicked.connect(lambda: self.switch_tab(2))
        sidebar_layout.addWidget(self.btn_nav_employees)

        sidebar_layout.addStretch(1)
        main_layout.addWidget(sidebar)

        # Контент
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setContentsMargins(32, 28, 32, 28)

        self.page_create_task = self.init_create_task_page()
        self.stacked_widget.addWidget(self.page_create_task)

        self.page_tasks_list = self.init_tasks_list_page()
        self.stacked_widget.addWidget(self.page_tasks_list)

        self.page_employees_list = self.init_employees_page()
        self.stacked_widget.addWidget(self.page_employees_list)

        main_layout.addWidget(self.stacked_widget, stretch=1)

        self.nav_buttons = [
            self.btn_nav_create,
            self.btn_nav_tasks,
            self.btn_nav_employees,
        ]

        self.switch_tab(0)
        self.load_profile_info()
        self.load_employees()

    def create_nav_button(self, text):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(42)
        btn.setStyleSheet(
            "QPushButton {"
            "   background-color: transparent;"
            "   color: #94a3b8;"
            "   border: none;"
            "   border-radius: 8px;"
            "   text-align: left;"
            "   padding-left: 14px;"
            "   font-size: 13.5px;"
            "   font-weight: 600;"
            "}"
            "QPushButton:hover {"
            "   background-color: rgba(255, 255, 255, 0.05);"
            "   color: #f8fafc;"
            "}"
        )
        return btn

    def switch_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)
        for idx, btn in enumerate(self.nav_buttons):
            if idx == index:
                btn.setStyleSheet(
                    "QPushButton {"
                    "   background-color: #6366f1;"
                    "   color: #ffffff;"
                    "   border: none;"
                    "   border-radius: 8px;"
                    "   text-align: left;"
                    "   padding-left: 14px;"
                    "   font-size: 13.5px;"
                    "   font-weight: 600;"
                    "}"
                )
            else:
                btn.setStyleSheet(
                    "QPushButton {"
                    "   background-color: transparent;"
                    "   color: #94a3b8;"
                    "   border: none;"
                    "   border-radius: 8px;"
                    "   text-align: left;"
                    "   padding-left: 14px;"
                    "   font-size: 13.5px;"
                    "   font-weight: 600;"
                    "}"
                    "QPushButton:hover {"
                    "   background-color: rgba(255, 255, 255, 0.05);"
                    "   color: #f8fafc;"
                    "}"
                )

        if index == 1:
            self.load_all_tasks()

    def init_create_task_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        title = QLabel("Создать новую задачу")
        title.setStyleSheet(
            "QLabel { font-size: 22px; font-weight: 800; color: #ffffff; border: none; background: transparent; }"
        )
        layout.addWidget(title)

        form_card = QFrame()
        form_card.setStyleSheet(
            "QFrame {"
            "   background-color: #111827;"
            "   border: 1px solid #1f293d;"
            "   border-radius: 14px;"
            "}"
        )
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(24, 20, 24, 20)
        form_layout.setSpacing(14)

        lbl_title = QLabel("Название задачи")
        lbl_title.setStyleSheet(
            "QLabel { color: #94a3b8; font-size: 13px; font-weight: 600; border: none; background: transparent; }"
        )
        form_layout.addWidget(lbl_title)

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Введите название задачи...")
        form_layout.addWidget(self.input_title)

        lbl_desc = QLabel("Описание")
        lbl_desc.setStyleSheet(
            "QLabel { color: #94a3b8; font-size: 13px; font-weight: 600; border: none; background: transparent; }"
        )
        form_layout.addWidget(lbl_desc)

        self.input_description = QTextEdit()
        self.input_description.setPlaceholderText(
            "Опишите подробные требования к задаче..."
        )
        self.input_description.setMaximumHeight(110)
        form_layout.addWidget(self.input_description)

        lbl_assigned = QLabel("Исполнитель")
        lbl_assigned.setStyleSheet(
            "QLabel { color: #94a3b8; font-size: 13px; font-weight: 600; border: none; background: transparent; }"
        )
        form_layout.addWidget(lbl_assigned)

        self.combo_assigned_to = QComboBox()
        form_layout.addWidget(self.combo_assigned_to)

        lbl_due = QLabel("Срок выполнения")
        lbl_due.setStyleSheet(
            "QLabel { color: #94a3b8; font-size: 13px; font-weight: 600; border: none; background: transparent; }"
        )
        form_layout.addWidget(lbl_due)

        self.create_date_picker = QDateEdit()
        self.create_date_picker.setCalendarPopup(True)
        self.create_date_picker.setDate(QDate.currentDate().addDays(3))
        form_layout.addWidget(self.create_date_picker)

        layout.addWidget(form_card)

        self.btn_create = QPushButton("Назначить задачу")
        self.btn_create.setCursor(Qt.PointingHandCursor)
        self.btn_create.setFixedHeight(44)
        self.btn_create.setStyleSheet(
            "QPushButton {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #4f46e5);"
            "   color: #ffffff;"
            "   border: none;"
            "   border-radius: 10px;"
            "   font-size: 14.5px;"
            "   font-weight: 700;"
            "}"
            "QPushButton:hover {"
            "   background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #4338ca);"
            "}"
        )
        self.btn_create.clicked.connect(self.create_task)
        layout.addWidget(self.btn_create)

        layout.addStretch(1)
        return page

    def init_tasks_list_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        title = QLabel("Мониторинг всех задач")
        title.setStyleSheet(
            "QLabel { font-size: 22px; font-weight: 800; color: #ffffff; border: none; background: transparent; }"
        )
        layout.addWidget(title)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(14)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.cards_container)
        layout.addWidget(self.scroll_area)

        return page

    def init_employees_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        header_layout = QHBoxLayout()

        title = QLabel("Команда и сотрудники")
        title.setStyleSheet(
            "QLabel { font-size: 22px; font-weight: 800; color: #ffffff; border: none; background: transparent; }"
        )
        header_layout.addWidget(title)

        header_layout.addStretch(1)

        filter_label = QLabel("Отдел:")
        filter_label.setStyleSheet(
            "QLabel { color: #94a3b8; font-size: 13.5px; font-weight: 500; border: none; background: transparent; }"
        )
        header_layout.addWidget(filter_label)

        self.combo_dept_filter = QComboBox()
        self.combo_dept_filter.setMinimumWidth(180)
        self.combo_dept_filter.currentIndexChanged.connect(self.filter_employees)
        header_layout.addWidget(self.combo_dept_filter)

        layout.addLayout(header_layout)

        self.emp_scroll_area = QScrollArea()
        self.emp_scroll_area.setWidgetResizable(True)

        self.emp_cards_container = QWidget()
        self.emp_cards_layout = QVBoxLayout(self.emp_cards_container)
        self.emp_cards_layout.setContentsMargins(0, 0, 0, 0)
        self.emp_cards_layout.setSpacing(12)
        self.emp_cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.emp_scroll_area.setWidget(self.emp_cards_container)
        layout.addWidget(self.emp_scroll_area)

        return page

    def load_profile_info(self):
        user = self.api_client.get_current_user_info()
        if user:
            display_name = user.get("username", "Менеджер")
            self.user_name_label.setText(display_name)
            self.avatar_label.setText(display_name[0].upper())

    def load_employees(self):
        self.all_users = self.api_client.get_users() or []
        departments = self.api_client.get_departments() or []

        self.combo_assigned_to.clear()

        self.combo_dept_filter.blockSignals(True)
        self.combo_dept_filter.clear()
        self.combo_dept_filter.addItem(" Все отделы", userData=None)

        for dept in departments:
            self.combo_dept_filter.addItem(
                f"🏢 {dept.get('name')}", userData=dept.get("id")
            )

        self.combo_dept_filter.blockSignals(False)

        if not self.all_users:
            self.combo_assigned_to.addItem("Нет доступных сотрудников", userData=None)
        else:
            for user in self.all_users:
                display_name = user.get("username", "")
                dept_info = user.get("department_detail") or {}
                dept_name = dept_info.get("name", "")

                first_name = user.get("first_name", "")
                last_name = user.get("last_name", "")

                if first_name or last_name:
                    display_name = (
                        f"{first_name} {last_name} (@{user.get('username')})"
                    )

                if dept_name:
                    display_name += f" — [{dept_name}]"

                self.combo_assigned_to.addItem(display_name, userData=user.get("id"))

        self.render_employee_cards(self.all_users)

    def filter_employees(self, index):
        selected_dept_id = self.combo_dept_filter.currentData()

        if selected_dept_id is None:
            filtered = self.all_users
        else:
            filtered = [
                u
                for u in self.all_users
                if u.get("department") == selected_dept_id
            ]

        self.render_employee_cards(filtered)

    def render_employee_cards(self, users_list):
        while self.emp_cards_layout.count():
            item = self.emp_cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not users_list:
            empty_lbl = QLabel("Сотрудники не найдены")
            empty_lbl.setStyleSheet(
                "QLabel { color: #64748b; font-size: 14px; padding: 20px; border: none; background: transparent; }"
            )
            self.emp_cards_layout.addWidget(empty_lbl)
            return

        for user in users_list:
            card = EmployeeCard(user)
            self.emp_cards_layout.addWidget(card)

    def create_task(self):
        """CRUD - Create"""
        title = self.input_title.text().strip()
        description = self.input_description.toPlainText().strip()
        assigned_to_id = self.combo_assigned_to.currentData()
        due_date = self.create_date_picker.date().toString("yyyy-MM-dd")

        if not title or assigned_to_id is None:
            QMessageBox.warning(
                self, "Ошибка", "Заполните название и выберите исполнителя."
            )
            return

        if self.api_client.create_task(
            title, description, assigned_to_id, due_date=due_date
        ):
            QMessageBox.information(self, "Успешно", "Задача успешно создана.")
            self.input_title.clear()
            self.input_description.clear()
            self.switch_tab(1)
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось создать задачу.")

    def load_all_tasks(self):
        """CRUD - Read List"""
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        tasks = self.api_client.get_tasks()
        if not tasks:
            empty_lbl = QLabel("Задач пока нет")
            empty_lbl.setStyleSheet(
                "QLabel { color: #64748b; font-size: 14px; padding: 20px; border: none; background: transparent; }"
            )
            self.cards_layout.addWidget(empty_lbl)
            return

        for task in tasks:
            card = ManagerTaskCard(
                task,
                on_edit_callback=self.open_edit_dialog,
                on_delete_callback=self.delete_task_confirm,
            )
            self.cards_layout.addWidget(card)

    def open_edit_dialog(self, task):
        """CRUD - Update"""
        dialog = EditTaskDialog(task, self.all_users, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data["title"]:
                QMessageBox.warning(
                    self, "Ошибка", "Название задачи не может быть пустым."
                )
                return

            success = self.api_client.update_task(
                task.get("id"),
                title=data["title"],
                description=data["description"],
                assigned_to=data["assigned_to"],
                due_date=data["due_date"],
            )

            if success:
                QMessageBox.information(self, "Успешно", "Задача обновлена.")
                self.load_all_tasks()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось обновить задачу.")

    def delete_task_confirm(self, task_id):
        """CRUD - Delete"""
        reply = QMessageBox.question(
            self,
            "Удаление задачи",
            f"Вы уверены, что хотите безвозвратно удалить задачу #{task_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.api_client.delete_task(task_id):
                QMessageBox.information(self, "Успешно", "Задача удалена.")
                self.load_all_tasks()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось удалить задачу.")