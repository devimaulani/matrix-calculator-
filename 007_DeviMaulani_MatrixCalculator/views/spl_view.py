from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit, QFrame, QSpinBox
from PyQt5.QtCore import Qt
import numpy as np

from widgets.dynamic_inputs import MatrixInputWidget, VectorInputWidget
from logic import spl_ops as so
from core.history import HISTORY


class SPLCalculatorPage(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self._last_use_snapshot = None  # (A_prev, b_prev)
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)

        # Header
        header = QHBoxLayout()
        title = QLabel("Kalkulator Sistem Persamaan Linear (SPL)")
        title.setStyleSheet("font-size:30px; font-weight:700;")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        header.addStretch()
        header.addWidget(title, alignment=Qt.AlignCenter)
        header.addStretch()
        btn_back = QPushButton("Kembali")
        btn_back.clicked.connect(lambda: self.navigate("welcome"))
        header.addWidget(btn_back)
        root.addLayout(header)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine); sep.setFrameShadow(QFrame.Sunken)
        root.addWidget(sep)

        # Method chooser
        row = QHBoxLayout()
        row.addWidget(QLabel("Metode:"))
        self.cb_method = QComboBox(); self.cb_method.addItems([
            "Eliminasi Gauss",
            "Eliminasi Gauss–Jordan",
            "Aturan Cramer",
            "Invers Matriks",
        ])
        row.addWidget(self.cb_method)
        row.addStretch()
        self.btn_calc = QPushButton("Selesaikan")
        self.btn_calc.clicked.connect(self._solve)
        row.addWidget(self.btn_calc)
        root.addLayout(row)

        # History controls
        hist = QHBoxLayout()
        hist.addWidget(QLabel("History:"))
        self.cb_hist = QComboBox()
        hist.addWidget(self.cb_hist)
        btn_refresh = QPushButton("Segarkan")
        btn_refresh.clicked.connect(self.refresh_history)
        hist.addWidget(btn_refresh)
        btn_use = QPushButton("Gunakan (A,b)")
        btn_use.clicked.connect(self._use_history)
        hist.addWidget(btn_use)
        btn_undo = QPushButton("Batalkan")
        btn_undo.clicked.connect(self._undo_history_use)
        hist.addWidget(btn_undo)
        btn_del = QPushButton("Hapus")
        btn_del.clicked.connect(self._delete_history)
        hist.addWidget(btn_del)
        hist.addStretch()
        root.addLayout(hist)

        # Inputs A and b
        ins = QHBoxLayout()
        self.A_widget = MatrixInputWidget(title="Matriks A (koefisien)", rows=3, cols=3)
        self.b_widget = VectorInputWidget(title="Vektor b (konstanta)", n=3)
        self.A_widget.row_spin.valueChanged.connect(self._sync_b_dim)
        ins.addWidget(self.A_widget)
        ins.addWidget(self.b_widget)
        root.addLayout(ins)

        # Result area
        self.result = QTextEdit(); self.result.setReadOnly(True)
        self.result.setStyleSheet("font-family: Consolas, monospace; font-size:14px;")
        root.addWidget(self.result)
        self.refresh_history()

    def _sync_b_dim(self):
        self.b_widget.dim_spin.setValue(self.A_widget.row_spin.value())

    def _fmt_vector(self, v: np.ndarray) -> str:
        return "[ " + ", ".join(f"{float(x):.6g}" for x in v.ravel()) + " ]"

    def _solve(self):
        try:
            A = self.A_widget.matrix()
            b = self.b_widget.vector()
            method = self.cb_method.currentText()

            if method == "Eliminasi Gauss":
                x, steps = so.gaussian_elimination(A, b)
                text = ["Solusi dengan Eliminasi Gauss:", self._fmt_vector(x), "", "Langkah-langkah:"] + steps
            elif method == "Eliminasi Gauss–Jordan":
                x, steps = so.gauss_jordan(A, b)
                text = ["Solusi dengan Gauss–Jordan:", self._fmt_vector(x), "", "Langkah-langkah:"] + steps
            elif method == "Aturan Cramer":
                x, steps = so.cramer(A, b)
                if x is None:
                    text = ["Aturan Cramer:", "Tidak ada solusi unik.", "", "Catatan:"] + steps
                else:
                    text = ["Aturan Cramer:", self._fmt_vector(x), "", "Langkah-langkah:"] + steps
            elif method == "Invers Matriks":
                x, steps = so.inverse_method(A, b)
                text = ["Metode Invers Matriks:", self._fmt_vector(x), "", "Langkah-langkah:"] + steps
            else:
                text = ["Metode tidak dikenal"]

            self.result.setText("\n".join(text))
            try:
                HISTORY.add_spl(A, b, method, steps, label=f"{method} ({A.shape[0]}x{A.shape[1]})")
                if 'x' in locals() and x is not None:
                    HISTORY.add_vector(np.array(x), label=f"Solusi x - {method}")
                self.refresh_history()
            except Exception:
                pass
        except Exception as e:
            self.result.setText(f"Error: {e}")

    def refresh_history(self):
        self.cb_hist.clear()
        for item in HISTORY.list_spl():
            self.cb_hist.addItem(item.label)

    def _use_history(self):
        idx = self.cb_hist.currentIndex()
        items = HISTORY.list_spl()
        if 0 <= idx < len(items):
            it = items[idx]
            # snapshot
            A_prev = self.A_widget.matrix()
            b_prev = self.b_widget.vector()
            self._last_use_snapshot = (A_prev, b_prev)
            self.A_widget.set_matrix(it.A)
            self.b_widget.set_vector(it.b)

    def _undo_history_use(self):
        if self._last_use_snapshot is None:
            return
        A_prev, b_prev = self._last_use_snapshot
        self.A_widget.set_matrix(A_prev)
        self.b_widget.set_vector(b_prev)
        self._last_use_snapshot = None

    def _delete_history(self):
        idx = self.cb_hist.currentIndex()
        if HISTORY.remove_spl(idx):
            self.refresh_history()

    def reset(self):
        self.cb_method.setCurrentIndex(0)
        self.A_widget.row_spin.setValue(3)
        self.A_widget.col_spin.setValue(3)
        self.b_widget.dim_spin.setValue(3)
        self.result.clear()
        try:
            self.A_widget.reset_values()
            self.b_widget.reset_values()
        except Exception:
            pass
