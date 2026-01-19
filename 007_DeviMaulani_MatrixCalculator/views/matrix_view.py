from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox, QTextEdit, QFrame
from PyQt5.QtCore import Qt
import numpy as np

from widgets.dynamic_inputs import MatrixInputWidget
from logic import matrix_ops as mo
from core.history import HISTORY


class MatrixCalculatorPage(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self._mat_widgets = []
        self._last_use_snapshot = None  # (index, np.ndarray)
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)

        # Header
        header = QHBoxLayout()
        title = QLabel("Kalkulator Matriks")
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

        # Controls
        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Operasi:"))
        self.cb_op = QComboBox(); self.cb_op.addItems(["Tambah", "Kurang", "Kali", "Transpose", "Analisis"])
        self.cb_op.currentTextChanged.connect(self._on_op_changed)
        ctrl.addWidget(self.cb_op)

        ctrl.addWidget(QLabel("Jumlah Matriks:"))
        self.sp_count = QSpinBox(); self.sp_count.setRange(1, 5); self.sp_count.setValue(2)
        self.sp_count.valueChanged.connect(self._rebuild_inputs)
        ctrl.addWidget(self.sp_count)
        ctrl.addStretch()

        self.btn_calc = QPushButton("Hitung")
        self.btn_calc.clicked.connect(self._calculate)
        ctrl.addWidget(self.btn_calc)
        root.addLayout(ctrl)

        # History controls
        hist = QHBoxLayout()
        hist.addWidget(QLabel("History:"))
        self.cb_hist = QComboBox()
        hist.addWidget(self.cb_hist)
        self.btn_hist_refresh = QPushButton("Segarkan")
        self.btn_hist_refresh.clicked.connect(self.refresh_history)
        hist.addWidget(self.btn_hist_refresh)
        hist.addSpacing(10)
        hist.addWidget(QLabel("Gunakan ke Matriks i:"))
        self.sp_hist_i = QSpinBox(); self.sp_hist_i.setRange(1, self.sp_count.value())
        self.sp_count.valueChanged.connect(lambda v: self.sp_hist_i.setMaximum(v))
        hist.addWidget(self.sp_hist_i)
        btn_use = QPushButton("Gunakan")
        btn_use.clicked.connect(self._use_history_to_index)
        hist.addWidget(btn_use)
        btn_add = QPushButton("Tambahkan sebagai baru")
        btn_add.clicked.connect(self._add_history_as_new)
        hist.addWidget(btn_add)
        btn_undo = QPushButton("Batalkan")
        btn_undo.clicked.connect(self._undo_history_use)
        hist.addWidget(btn_undo)
        btn_del = QPushButton("Hapus")
        btn_del.clicked.connect(self._delete_history)
        hist.addWidget(btn_del)
        hist.addStretch()
        root.addLayout(hist)

        # Matrices area
        self.inputs_area = QVBoxLayout()
        root.addLayout(self.inputs_area)

        # Result area
        self.result = QTextEdit(); self.result.setReadOnly(True)
        self.result.setStyleSheet("font-family: Consolas, monospace; font-size:14px;")
        root.addWidget(self.result)

        self._rebuild_inputs()
        self._on_op_changed(self.cb_op.currentText())
        self.refresh_history()

    def _on_op_changed(self, op: str):
        if op in ("Transpose", "Analisis"):
            self.sp_count.setValue(1)
            self.sp_count.setEnabled(False)
        else:
            self.sp_count.setEnabled(True)

    def _rebuild_inputs(self):
        # Clear
        for i in reversed(range(self.inputs_area.count())):
            item = self.inputs_area.takeAt(i)
            w = item.widget()
            if w is not None:
                w.setParent(None)
        self._mat_widgets.clear()
        # Build
        for idx in range(self.sp_count.value()):
            w = MatrixInputWidget(title=f"Matriks {chr(ord('A')+idx)}")
            self.inputs_area.addWidget(w)
            self._mat_widgets.append(w)

    def _fmt_matrix(self, A: np.ndarray) -> str:
        rows = ["[ " + "\t".join(f"{x:8.4g}" for x in row) + " ]" for row in A]
        return "\n".join(rows)

    def _calculate(self):
        try:
            op = self.cb_op.currentText()
            mats = [w.matrix() for w in self._mat_widgets]

            if op == "Tambah":
                res = mats[0].copy()
                for m in mats[1:]:
                    res = mo.add(res, m)
                text = "Hasil penjumlahan:\n" + self._fmt_matrix(res)

            elif op == "Kurang":
                res = mats[0].copy()
                for m in mats[1:]:
                    res = mo.sub(res, m)
                text = "Hasil pengurangan:\n" + self._fmt_matrix(res)

            elif op == "Kali":
                res = mats[0].copy()
                for m in mats[1:]:
                    res = mo.mul(res, m)
                text = "Hasil perkalian berantai:\n" + self._fmt_matrix(res)

            elif op == "Transpose":
                res = mo.transpose(mats[0])
                text = "Transpose matriks A:\n" + self._fmt_matrix(res)

            elif op == "Analisis":
                info = mo.analyze(mats[0])
                lines = ["Analisis matriks A:"]
                for k, v in info.items():
                    if isinstance(v, float):
                        lines.append(f"- {k}: {v:.6g}")
                    else:
                        lines.append(f"- {k}: {v}")
                text = "\n".join(lines)
                self.result.setText(text)
                self._set_success_style()
                # save first matrix to history
                try:
                    A0 = mats[0]
                    HISTORY.add_matrix(A0, label=f"Analisis {A0.shape[0]}x{A0.shape[1]}")
                    self.refresh_history()
                except Exception:
                    pass
                return
            else:
                text = "Operasi tidak dikenal"

            self.result.setText(text)
            self._set_success_style()
            # Save result to history
            try:
                HISTORY.add_matrix(res, label=f"{op} {res.shape[0]}x{res.shape[1]}")
                self.refresh_history()
            except Exception:
                pass
        except Exception as e:
            self.result.setText(f"Error: {e}")
            self._set_error_style()

    def _set_success_style(self):
        self.result.setStyleSheet(
            "font-family: Consolas, monospace; font-size:14px; background:#E8F5E9; color:#1B5E20; border:2px solid #8FB996;"
        )

    def _set_error_style(self):
        self.result.setStyleSheet(
            "font-family: Consolas, monospace; font-size:14px; background:#FCEAEA; color:#B71C1C; border:2px solid #E57373;"
        )

    def refresh_history(self):
        self.cb_hist.clear()
        for item in HISTORY.list_matrix():
            self.cb_hist.addItem(item.label)

    def _use_history_to_index(self):
        idx = self.cb_hist.currentIndex()
        items = HISTORY.list_matrix()
        if 0 <= idx < len(items):
            arr = items[idx].data
            target = self.sp_hist_i.value() - 1
            if target >= self.sp_count.value():
                self.sp_count.setValue(target + 1)
            # snapshot before apply
            prev = self._mat_widgets[target].matrix()
            self._last_use_snapshot = (target, prev)
            self._mat_widgets[target].set_matrix(arr)

    def _add_history_as_new(self):
        idx = self.cb_hist.currentIndex()
        items = HISTORY.list_matrix()
        if 0 <= idx < len(items):
            arr = items[idx].data
            current = self.sp_count.value()
            self.sp_count.setValue(current + 1)
            self._mat_widgets[-1].set_matrix(arr)

    def _undo_history_use(self):
        if self._last_use_snapshot is None:
            return
        target, prev = self._last_use_snapshot
        if target < self.sp_count.value():
            self._mat_widgets[target].set_matrix(prev)
        self._last_use_snapshot = None

    def _delete_history(self):
        idx = self.cb_hist.currentIndex()
        if HISTORY.remove_matrix(idx):
            self.refresh_history()

    def _swap_matrices(self):
        n = self.sp_count.value()
        i = self.sp_swap_i.value() - 1
        j = self.sp_swap_j.value() - 1
        if i == j or i < 0 or j < 0 or i >= n or j >= n:
            return
        Ai = self._mat_widgets[i].matrix()
        Aj = self._mat_widgets[j].matrix()
        self._mat_widgets[i].set_matrix(Aj)
        self._mat_widgets[j].set_matrix(Ai)

    def reset(self):
        self.cb_op.setCurrentIndex(0)
        self.sp_count.setValue(2)
        self.result.clear()
        self._rebuild_inputs()
