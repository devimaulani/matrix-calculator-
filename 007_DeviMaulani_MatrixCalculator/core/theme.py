def app_stylesheet():
    cream = "#F7F2E9"
    green = "#5E8C61"
    darkg = "#3D5A40"
    accent = "#8FB996"
    text = "#233D26"
    return f"""
    * {{
        font-family: 'Segoe UI', Arial, sans-serif;
        color: {text};
    }}
    QMainWindow {{
        background-color: {cream};
    }}
    QWidget {{
        background-color: {cream};
        font-size: 15px;
    }}
    QLabel#title {{
        font-size: 26px;
        font-weight: 800;
        color: {darkg};
    }}
    QPushButton {{
        background-color: {green};
        color: white;
        border: none;
        padding: 12px 22px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 16px;
        min-height: 46px;
        min-width: 180px;
    }}
    QPushButton:hover {{
        background-color: {darkg};
    }}
    QPushButton:pressed {{
        background-color: #2c4230;
    }}
    QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit, QTextEdit {{
        background: white;
        border: 3px solid {accent};
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 15px;
    }}
    QComboBox {{
        min-height: 42px;
        min-width: 240px;
        padding-right: 32px;
    }}
    QComboBox QAbstractItemView {{
        font-size: 15px;
        selection-background-color: #DFF1E0;
        selection-color: {text};
    }}
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus, QComboBox:focus {{
        border-color: {darkg};
    }}
    QGroupBox {{
        border: 2px solid {accent};
        border-radius: 10px;
        margin-top: 12px;
        padding: 10px;
        font-weight: 700;
    }}
    QTableView {{
        gridline-color: {darkg};
        selection-background-color: #DFF1E0;
        selection-color: {text};
    }}
    QFrame[frameShape="4"] {{ /* HLine */
        border: none; border-top: 2px solid {accent}; margin: 8px 0;
    }}
    """
