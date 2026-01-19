from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import numpy as np


def _to_float(text: str) -> float:
    try:
        return float(text)
    except Exception:
        return 0.0


class MatrixInputWidget(QWidget):
    def __init__(self, rows: int = 2, cols: int = 2, title: str = "Matriks"):
        super().__init__()
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        top = QHBoxLayout()
        top.addWidget(QLabel(title))
        top.addWidget(QLabel("Baris"))
        self.row_spin = QSpinBox(); self.row_spin.setRange(1, 10); self.row_spin.setValue(rows)
        top.addWidget(self.row_spin)
        top.addWidget(QLabel("Kolom"))
        self.col_spin = QSpinBox(); self.col_spin.setRange(1, 10); self.col_spin.setValue(cols)
        top.addWidget(self.col_spin)
        top.addStretch()
        self._layout.addLayout(top)

        self.table = QTableWidget(rows, cols)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self._layout.addWidget(self.table)

        self.row_spin.valueChanged.connect(self._resize)
        self.col_spin.valueChanged.connect(self._resize)
        self._fill_zero()

    def _fill_zero(self):
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                if not self.table.item(i, j):
                    self.table.setItem(i, j, QTableWidgetItem("0"))

    def _resize(self):
        r, c = self.row_spin.value(), self.col_spin.value()
        self.table.setRowCount(r)
        self.table.setColumnCount(c)
        self._fill_zero()

    def matrix(self) -> np.ndarray:
        r, c = self.table.rowCount(), self.table.columnCount()
        data = np.zeros((r, c), dtype=float)
        for i in range(r):
            for j in range(c):
                item = self.table.item(i, j)
                data[i, j] = _to_float(item.text() if item else "0")
        return data

    def set_matrix(self, arr: np.ndarray):
        r, c = arr.shape
        self.row_spin.setValue(int(r))
        self.col_spin.setValue(int(c))
        for i in range(r):
            for j in range(c):
                self.table.setItem(i, j, QTableWidgetItem(str(arr[i, j])))

    def reset_values(self):
        r, c = self.table.rowCount(), self.table.columnCount()
        for i in range(r):
            for j in range(c):
                self.table.setItem(i, j, QTableWidgetItem("0"))


class VectorInputWidget(QWidget):
    def __init__(self, n: int = 3, title: str = "Vektor"):
        super().__init__()
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        top = QHBoxLayout()
        top.addWidget(QLabel(title))
        top.addWidget(QLabel("Dimensi"))
        self.dim_spin = QSpinBox(); self.dim_spin.setRange(1, 10); self.dim_spin.setValue(n)
        top.addWidget(self.dim_spin)
        top.addStretch()
        self._layout.addLayout(top)

        self.table = QTableWidget(n, 1)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self._layout.addWidget(self.table)

        self.dim_spin.valueChanged.connect(self._resize)
        self._fill_zero()

    def _fill_zero(self):
        for i in range(self.table.rowCount()):
            if not self.table.item(i, 0):
                self.table.setItem(i, 0, QTableWidgetItem("0"))

    def _resize(self):
        n = self.dim_spin.value()
        self.table.setRowCount(n)
        self._fill_zero()

    def vector(self) -> np.ndarray:
        n = self.table.rowCount()
        data = np.zeros(n, dtype=float)
        for i in range(n):
            item = self.table.item(i, 0)
            data[i] = _to_float(item.text() if item else "0")
        return data

    def set_vector(self, v: np.ndarray):
        n = int(v.shape[0])
        self.dim_spin.setValue(n)
        for i in range(n):
            self.table.setItem(i, 0, QTableWidgetItem(str(float(v[i]))))

    def reset_values(self):
        n = self.table.rowCount()
        for i in range(n):
            self.table.setItem(i, 0, QTableWidgetItem("0"))
