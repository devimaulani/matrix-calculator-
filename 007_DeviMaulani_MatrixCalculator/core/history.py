from dataclasses import dataclass
from typing import List, Any, Optional, Dict
import json
import os
import numpy as np


@dataclass
class MatrixHistoryItem:
    data: np.ndarray
    label: str


@dataclass
class VectorHistoryItem:
    data: np.ndarray
    label: str


@dataclass
class SPLHistoryItem:
    A: np.ndarray
    b: np.ndarray
    method: str
    label: str
    steps: Optional[List[str]] = None


class HistoryManager:
    def __init__(self, limit: int = 50, storage_path: Optional[str] = None):
        self.limit = limit
        self._matrix: List[MatrixHistoryItem] = []
        self._vector: List[VectorHistoryItem] = []
        self._spl: List[SPLHistoryItem] = []
        # default persistent storage location in user home
        home = os.path.expanduser("~")
        default_name = ".kalkulator_aljabar_history.json"
        self.storage_path = storage_path or os.path.join(home, default_name)
        # try load existing history
        try:
            if os.path.exists(self.storage_path):
                self.load_from_file(self.storage_path)
        except Exception:
            # ignore load errors to avoid blocking app startup
            pass

    # Matrix
    def add_matrix(self, arr: np.ndarray, label: Optional[str] = None):
        label = label or f"Matriks {arr.shape[0]}x{arr.shape[1]}"
        self._matrix.insert(0, MatrixHistoryItem(arr.copy(), label))
        self._matrix = self._matrix[: self.limit]
        self._autosave()

    def list_matrix(self) -> List[MatrixHistoryItem]:
        return list(self._matrix)
    
    def remove_matrix(self, idx: int) -> bool:
        if 0 <= idx < len(self._matrix):
            del self._matrix[idx]
            self._autosave()
            return True
        return False

    # Vector
    def add_vector(self, vec: np.ndarray, label: Optional[str] = None):
        label = label or f"Vektor dim {vec.shape[0]}"
        self._vector.insert(0, VectorHistoryItem(vec.copy(), label))
        self._vector = self._vector[: self.limit]
        self._autosave()

    def list_vector(self) -> List[VectorHistoryItem]:
        return list(self._vector)
    
    def remove_vector(self, idx: int) -> bool:
        if 0 <= idx < len(self._vector):
            del self._vector[idx]
            self._autosave()
            return True
        return False

    # SPL
    def add_spl(self, A: np.ndarray, b: np.ndarray, method: str, steps: Optional[List[str]] = None, label: Optional[str] = None):
        label = label or f"SPL {A.shape[0]}x{A.shape[1]} (metode {method})"
        self._spl.insert(0, SPLHistoryItem(A.copy(), b.copy(), method, label, steps or []))
        self._spl = self._spl[: self.limit]
        self._autosave()

    def list_spl(self) -> List[SPLHistoryItem]:
        return list(self._spl)
    
    def remove_spl(self, idx: int) -> bool:
        if 0 <= idx < len(self._spl):
            del self._spl[idx]
            self._autosave()
            return True
        return False

    # Export utilities
    def to_dict(self) -> Dict[str, Any]:
        return {
            "matrix": [
                {"label": it.label, "data": it.data.tolist()} for it in self._matrix
            ],
            "vector": [
                {"label": it.label, "data": it.data.tolist()} for it in self._vector
            ],
            "spl": [
                {
                    "label": it.label,
                    "method": it.method,
                    "A": it.A.tolist(),
                    "b": it.b.tolist(),
                    "steps": list(it.steps or []),
                }
                for it in self._spl
            ],
        }

    def export_to_file(self, file_path: str):
        payload = self.to_dict()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    # Persistent storage helpers
    def save_to_file(self, file_path: Optional[str] = None):
        path = file_path or self.storage_path
        payload = self.to_dict()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load_from_file(self, file_path: Optional[str] = None):
        path = file_path or self.storage_path
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # reconstruct lists
        self._matrix = [
            MatrixHistoryItem(np.array(item.get("data", []), dtype=float), item.get("label", "Matriks"))
            for item in data.get("matrix", [])
        ]
        self._vector = [
            VectorHistoryItem(np.array(item.get("data", []), dtype=float), item.get("label", "Vektor"))
            for item in data.get("vector", [])
        ]
        self._spl = []
        for item in data.get("spl", []):
            A = np.array(item.get("A", []), dtype=float)
            b = np.array(item.get("b", []), dtype=float)
            method = item.get("method", "")
            label = item.get("label", "SPL")
            steps = item.get("steps", [])
            self._spl.append(SPLHistoryItem(A, b, method, label, steps))

    def _autosave(self):
        try:
            self.save_to_file()
        except Exception:
            pass


# Singleton instance
HISTORY = HistoryManager()
