from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QFrame
from PyQt5.QtCore import Qt
from core.state import APP_STATE


class QuizSetupPage(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self.selected_level = APP_STATE.quiz_level
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        # Header
        header = QHBoxLayout()
        title = QLabel("Pilih Level Kuis")
        title.setStyleSheet("font-size:30px; font-weight:700;")
        title.setAlignment(Qt.AlignCenter)
        header.addStretch(); header.addWidget(title, alignment=Qt.AlignCenter); header.addStretch()
        root.addLayout(header)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setFrameShadow(QFrame.Sunken)
        root.addWidget(sep)

        # Level buttons
        row_levels = QHBoxLayout()
        btn_easy = QPushButton("Easy")
        btn_med = QPushButton("Medium")
        btn_hard = QPushButton("Hard")
        for b in (btn_easy, btn_med, btn_hard):
            b.setMinimumHeight(56)
            b.clicked.connect(lambda _, x=b.text(): self._choose_level(x))
        row_levels.addWidget(btn_easy)
        row_levels.addWidget(btn_med)
        row_levels.addWidget(btn_hard)
        root.addLayout(row_levels)

        # Question count selector
        row_count = QHBoxLayout()
        row_count.addWidget(QLabel("Jumlah Soal (5-15):"))
        self.sp_count = QSpinBox(); self.sp_count.setRange(5, 15); self.sp_count.setValue(APP_STATE.quiz_count)
        row_count.addWidget(self.sp_count)
        row_count.addStretch()
        root.addLayout(row_count)

        # Start button
        row_start = QHBoxLayout()
        btn_start = QPushButton("Mulai")
        btn_start.clicked.connect(self._start_quiz)
        row_start.addWidget(btn_start)
        row_start.addStretch()
        root.addLayout(row_start)

        # Back button
        row_back = QHBoxLayout()
        btn_back = QPushButton("Kembali")
        btn_back.clicked.connect(lambda: self.navigate("welcome"))
        row_back.addWidget(btn_back)
        row_back.addStretch()
        root.addLayout(row_back)

    def _choose_level(self, level: str):
        self.selected_level = level
        APP_STATE.quiz_count = self.sp_count.value()
        APP_STATE.quiz_level = self.selected_level
        self.navigate("quiz")

    def _start_quiz(self):
        APP_STATE.quiz_level = self.selected_level
        APP_STATE.quiz_count = self.sp_count.value()
        self.navigate("quiz")
