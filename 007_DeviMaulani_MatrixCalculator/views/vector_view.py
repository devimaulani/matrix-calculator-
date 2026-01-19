from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QDoubleSpinBox, QTextEdit, QFrame, QSpinBox
from PyQt5.QtCore import Qt
import numpy as np

from widgets.dynamic_inputs import VectorInputWidget
from logic import vector_ops as vo
from core.history import HISTORY


class VectorCalculatorPage(QWidget):
    def __init__(self, navigate):
        super().__init__()
        self.navigate = navigate
        self._vec_widgets = []
        self._coef_spins = []
        self._last_use_snapshot = None  # (index, vector)
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)

        # Header
        header = QHBoxLayout()
        title = QLabel("Kalkulator Vektor")
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

        # Operation chooser
        op_row = QHBoxLayout()
        op_row.addWidget(QLabel("Operasi:"))
        self.cb_op = QComboBox(); self.cb_op.addItems([
            "Jumlah (Σ v_i)",
            "Selisih berantai",
            "Kombinasi linear",
            "Ekspresi a·v1 + b·v2",
            "Dot product v1·v2",
            "Cross product v1×v2 (3D)",
            "Norma v_k",
            "Proyeksi v1 ke arah v2",
            "Sudut antara v1 dan v2",
        ])
        self.cb_op.currentTextChanged.connect(self._on_op_changed)
        op_row.addWidget(self.cb_op)

        # Dynamic count
        op_row.addSpacing(12)
        op_row.addWidget(QLabel("Jumlah Vektor:"))
        self.sp_count = QSpinBox(); self.sp_count.setRange(1, 6); self.sp_count.setValue(2)
        self.sp_count.valueChanged.connect(self._rebuild_inputs)
        op_row.addWidget(self.sp_count)

        # Coefficient panel for linear combination
        op_row.addSpacing(12)
        self.lbl_coef = QLabel("Koef (c_i):")
        op_row.addWidget(self.lbl_coef)
        self.coef_panel = QHBoxLayout()
        op_row.addLayout(self.coef_panel)

        # Scalars for 2-vector expression a*v1 + b*v2
        op_row.addSpacing(12)
        self.lbl_ab = QLabel("a, b:")
        op_row.addWidget(self.lbl_ab)
        self.sp_a = QDoubleSpinBox(); self.sp_a.setRange(-1e9, 1e9); self.sp_a.setSingleStep(0.1); self.sp_a.setValue(3.0)
        self.sp_b = QDoubleSpinBox(); self.sp_b.setRange(-1e9, 1e9); self.sp_b.setSingleStep(0.1); self.sp_b.setValue(-2.0)
        op_row.addWidget(self.sp_a)
        op_row.addWidget(self.sp_b)

        # Index for norm
        op_row.addSpacing(12)
        self.lbl_k = QLabel("k:")
        op_row.addWidget(self.lbl_k)
        self.sp_k = QSpinBox(); self.sp_k.setRange(1, self.sp_count.value())
        self.sp_count.valueChanged.connect(lambda v: self.sp_k.setMaximum(v))
        op_row.addWidget(self.sp_k)

        op_row.addStretch()
        self.btn_calc = QPushButton("Hitung")
        self.btn_calc.clicked.connect(self._calculate)
        op_row.addWidget(self.btn_calc)
        root.addLayout(op_row)

        # History controls
        hist = QHBoxLayout()
        hist.addWidget(QLabel("History:"))
        self.cb_hist = QComboBox()
        hist.addWidget(self.cb_hist)
        btn_refresh = QPushButton("Segarkan")
        btn_refresh.clicked.connect(self.refresh_history)
        hist.addWidget(btn_refresh)
        hist.addSpacing(10)
        hist.addWidget(QLabel("Gunakan ke vektor i:"))
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

        # Inputs
        self.inputs_area = QHBoxLayout()
        root.addLayout(self.inputs_area)

        # Result
        self.result = QTextEdit(); self.result.setReadOnly(True)
        self.result.setStyleSheet("font-family: Consolas, monospace; font-size:14px;")
        root.addWidget(self.result)

        self._rebuild_inputs()
        self._on_op_changed(self.cb_op.currentText())
        self.refresh_history()

    def _fmt_vector(self, v: np.ndarray) -> str:
        return "[ " + ", ".join(f"{float(x):.6g}" for x in v.ravel()) + " ]"

    def _on_op_changed(self, op: str):
        is_lin = (op == "Kombinasi linear")
        is_expr2 = (op == "Ekspresi a·v1 + b·v2")
        is_norm = (op == "Norma v_k")
        # Toggle coefficient inputs and k index
        self.lbl_coef.setVisible(is_lin)
        for s in self._coef_spins:
            s.setVisible(is_lin)
        self.lbl_ab.setVisible(is_expr2)
        self.sp_a.setVisible(is_expr2)
        self.sp_b.setVisible(is_expr2)
        self.lbl_k.setVisible(is_norm)
        self.sp_k.setVisible(is_norm)
        # Ops requiring exactly 2 vectors
        needs_two = op in ("Ekspresi a·v1 + b·v2", "Dot product v1·v2", "Cross product v1×v2 (3D)", "Proyeksi v1 ke arah v2", "Sudut antara v1 dan v2")
        if needs_two:
            self.sp_count.setValue(2)
            self.sp_count.setEnabled(False)
        else:
            self.sp_count.setEnabled(True)

    def _calculate(self):
        try:
            op = self.cb_op.currentText()
            vecs = [w.vector() for w in self._vec_widgets]

            if op == "Jumlah (Σ v_i)":
                # All vectors must have same shape
                base = vecs[0].copy()
                for v in vecs[1:]:
                    base = vo.add(base, v)
                res = base
                text = "Σ v_i = " + self._fmt_vector(res)
            elif op == "Selisih berantai":
                base = vecs[0].copy()
                for v in vecs[1:]:
                    base = vo.sub(base, v)
                res = base
                text = "v1 - v2 - ... - vn = " + self._fmt_vector(res)
            elif op == "Kombinasi linear":
                # sum c_i v_i
                res = np.zeros_like(vecs[0], dtype=float)
                for coef, v in zip([s.value() for s in self._coef_spins], vecs):
                    if v.shape != res.shape:
                        raise ValueError("Dimensi vektor harus sama untuk kombinasi linear")
                    res = res + coef * v
                text = "Σ c_i v_i = " + self._fmt_vector(res)
            elif op == "Ekspresi a·v1 + b·v2":
                if len(vecs) != 2:
                    raise ValueError("Operasi ini membutuhkan tepat 2 vektor")
                if vecs[0].shape != vecs[1].shape:
                    raise ValueError("Dimensi vektor harus sama untuk operasi ini")
                a = self.sp_a.value()
                b = self.sp_b.value()
                res = a * vecs[0] + b * vecs[1]
                text = f"a·v1 + b·v2 = {self._fmt_vector(res)} (a={a:.6g}, b={b:.6g})"
            elif op == "Dot product v1·v2":
                if len(vecs) != 2:
                    raise ValueError("Dot product membutuhkan tepat 2 vektor")
                val = vo.dot(vecs[0], vecs[1])
                text = f"v1·v2 = {val:.6g}"
                self.result.setText(text)
                self._set_success_style()
                try:
                    HISTORY.add_vector(np.array([val], dtype=float), label="Dot product v1·v2")
                    self.refresh_history()
                except Exception:
                    pass
                return
            elif op == "Cross product v1×v2 (3D)":
                if len(vecs) != 2:
                    raise ValueError("Cross product membutuhkan tepat 2 vektor")
                res = vo.cross(vecs[0], vecs[1])
                text = "v1×v2 = " + self._fmt_vector(res)
            elif op == "Norma v_k":
                k = self.sp_k.value()
                if not (1 <= k <= len(vecs)):
                    raise ValueError("k di luar rentang jumlah vektor")
                val = vo.norm(vecs[k-1])
                text = f"||v{k}|| = {val:.6g}"
                self.result.setText(text)
                self._set_success_style()
                try:
                    HISTORY.add_vector(np.array([val], dtype=float), label=f"Norma v{k}")
                    self.refresh_history()
                except Exception:
                    pass
                return
            elif op == "Proyeksi v1 ke arah v2":
                if len(vecs) != 2:
                    raise ValueError("Proyeksi membutuhkan tepat 2 vektor")
                res = vo.projection_u_on_v(vecs[0], vecs[1])
                text = "proj_{v2}(v1) = " + self._fmt_vector(res)
            elif op == "Sudut antara v1 dan v2":
                if len(vecs) != 2:
                    raise ValueError("Sudut membutuhkan tepat 2 vektor")
                deg = vo.angle_between(vecs[0], vecs[1])
                text = f"∠(v1,v2) = {deg:.6g} derajat"
                self.result.setText(text)
                self._set_success_style()
                try:
                    HISTORY.add_vector(np.array([deg], dtype=float), label="Sudut(v1,v2) [deg]")
                    self.refresh_history()
                except Exception:
                    pass
                return
            else:
                text = "Operasi tidak dikenal"

            self.result.setText(text)
            self._set_success_style()
            # save to history
            try:
                HISTORY.add_vector(res, label=f"Hasil {op}")
                self.refresh_history()
            except Exception:
                pass
        except Exception as e:
            self.result.setText(f"Error: {e}")
            self._set_error_style()

    def _rebuild_inputs(self):
        # clear
        for i in reversed(range(self.inputs_area.count())):
            item = self.inputs_area.takeAt(i)
            w = item.widget()
            if w is not None:
                w.setParent(None)
        self._vec_widgets.clear()

        # rebuild vector widgets
        for idx in range(self.sp_count.value()):
            w = VectorInputWidget(title=f"Vektor v{idx+1}")
            self.inputs_area.addWidget(w)
            self._vec_widgets.append(w)

        # rebuild coef spins to match count
        for s in self._coef_spins:
            s.deleteLater()
        self._coef_spins = []
        for idx in range(self.sp_count.value()):
            s = QDoubleSpinBox(); s.setRange(-1e9, 1e9); s.setSingleStep(0.1); s.setValue(1.0 if idx==0 else 1.0)
            self.coef_panel.addWidget(s)
            self._coef_spins.append(s)
        self._on_op_changed(self.cb_op.currentText())

    def refresh_history(self):
        self.cb_hist.clear()
        for item in HISTORY.list_vector():
            self.cb_hist.addItem(item.label)

    def _use_history_to_index(self):
        idx = self.cb_hist.currentIndex()
        items = HISTORY.list_vector()
        if 0 <= idx < len(items):
            v = items[idx].data
            target = self.sp_hist_i.value() - 1
            if target >= self.sp_count.value():
                self.sp_count.setValue(target + 1)
            prev = self._vec_widgets[target].vector()
            self._last_use_snapshot = (target, prev)
            self._vec_widgets[target].set_vector(v)

    def _add_history_as_new(self):
        idx = self.cb_hist.currentIndex()
        items = HISTORY.list_vector()
        if 0 <= idx < len(items):
            v = items[idx].data
            current = self.sp_count.value()
            self.sp_count.setValue(current + 1)
            self._vec_widgets[-1].set_vector(v)

    def _undo_history_use(self):
        if self._last_use_snapshot is None:
            return
        target, prev = self._last_use_snapshot
        if target < self.sp_count.value():
            self._vec_widgets[target].set_vector(prev)
        self._last_use_snapshot = None

    def _delete_history(self):
        idx = self.cb_hist.currentIndex()
        if HISTORY.remove_vector(idx):
            self.refresh_history()

    def reset(self):
        self.cb_op.setCurrentIndex(0)
        self.sp_count.setValue(2)
        self.sp_k.setValue(1)
        self.result.clear()
        self._rebuild_inputs()

    def _set_success_style(self):
        self.result.setStyleSheet(
            "font-family: Consolas, monospace; font-size:14px; background:#E8F5E9; color:#1B5E20; border:2px solid #8FB996;"
        )

    def _set_error_style(self):
        self.result.setStyleSheet(
            "font-family: Consolas, monospace; font-size:14px; background:#FCEAEA; color:#B71C1C; border:2px solid #E57373;"
        )
