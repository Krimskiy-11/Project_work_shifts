DARK_THEME = """
/* === Глобальные настройки === */
QWidget {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: "Segoe UI", "Inter", -apple-system, sans-serif;
    font-size: 13px;
}

/* === Боковое меню (Sidebar) === */
QFrame[class="sidebar"] {
    background-color: #1e293b;
    border-right: 1px solid #334155;
}

/* Кнопки навигации */
QPushButton[class="nav-btn"] {
    background-color: transparent;
    color: #94a3b8;
    font-size: 14px;
    font-weight: 600;
    text-align: left;
    padding: 12px 16px;
    border: none;
    border-radius: 10px;
}

QPushButton[class="nav-btn"]:hover {
    background-color: #334155;
    color: #f8fafc;
}

QPushButton[class="nav-btn"][active="true"] {
    background-color: #6366f1;
    color: #ffffff;
}

/* Компактный аватар и профиль в меню */
QLabel[class="sidebar-avatar"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #a855f7);
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    border-radius: 22px;
    min-width: 44px;
    max-width: 44px;
    min-height: 44px;
    max-height: 44px;
}

QLabel[class="sidebar-name"] {
    font-size: 14px;
    font-weight: 700;
    color: #ffffff;
}

QLabel[class="sidebar-role"] {
    font-size: 12px;
    color: #818cf8;
}

/* Поля ввода и кнопки */
QLineEdit, QTextEdit, QComboBox {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 10px;
}

QPushButton[class="primary-btn"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #4f46e5);
    color: #ffffff;
    font-weight: 600;
    border-radius: 10px;
    padding: 11px 20px;
}
"""