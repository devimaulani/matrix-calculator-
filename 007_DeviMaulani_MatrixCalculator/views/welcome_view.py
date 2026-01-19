from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from core.history import HISTORY


class WelcomePage(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Kalkulator Aljabar Linear")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 700;")
        title.setObjectName("title")
        subtitle = QLabel("Matriks • Sistem Persamaan Linear • Vektor")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color:#555; margin-bottom: 12px;")

        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setFrameShadow(QFrame.Sunken)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(sep)

        buttons = QHBoxLayout()
        btn_matrix = QPushButton("Kalkulator Matriks")
        btn_spl = QPushButton("Kalkulator SPL")
        btn_vector = QPushButton("Kalkulator Vektor")
        for b in (btn_matrix, btn_spl, btn_vector):
            b.setMinimumHeight(48)
            b.setStyleSheet("font-size:16px; padding:10px 16px;")
        btn_matrix.clicked.connect(lambda: self.navigate("matrix"))
        btn_spl.clicked.connect(lambda: self.navigate("spl"))
        btn_vector.clicked.connect(lambda: self.navigate("vector"))

        buttons.addWidget(btn_matrix)
        buttons.addWidget(btn_spl)
        buttons.addWidget(btn_vector)
        layout.addLayout(buttons)

        # Second row: Quiz and Export
        row2 = QHBoxLayout()
        btn_quiz = QPushButton("Kuis Interaktif")
        btn_export = QPushButton("Export History")
        btn_quiz.clicked.connect(lambda: self.navigate("quiz_setup"))
        btn_export.clicked.connect(self._export_history)
        row2.addWidget(btn_quiz)
        row2.addWidget(btn_export)
        layout.addLayout(row2)

        foot = QLabel("Selamat datang! Pilih jenis kalkulator untuk memulai.")
        foot.setAlignment(Qt.AlignCenter)
        foot.setStyleSheet("color:#777; margin-top: 20px;")
        layout.addWidget(foot)

    def _export_history(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan History ke JSON", "history.json", "JSON Files (*.json)")
        if not path:
            return
        try:
            HISTORY.export_to_file(path)
            QMessageBox.information(self, "Sukses", f"History berhasil diexport ke:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan history: {e}")
