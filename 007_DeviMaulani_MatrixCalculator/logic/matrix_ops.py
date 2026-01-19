import numpy as np


def add(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    if A.shape != B.shape:
        raise ValueError(f"Ukuran matriks harus sama: {A.shape} vs {B.shape}")
    return A + B


def sub(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    if A.shape != B.shape:
        raise ValueError(f"Ukuran matriks harus sama: {A.shape} vs {B.shape}")
    return A - B


def mul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    if A.shape[1] != B.shape[0]:
        raise ValueError(f"Kolom A harus sama dengan baris B: {A.shape} x {B.shape}")
    return A @ B


def transpose(A: np.ndarray) -> np.ndarray:
    return A.T


def analyze(A: np.ndarray) -> dict:
    info = {}
    r, c = A.shape
    info["ukuran"] = f"{r} x {c}"
    info["persegi"] = (r == c)
    info["nol"] = np.allclose(A, 0)
    info["diagonal"] = bool(r == c and np.allclose(A, np.diag(np.diag(A))))
    info["identitas"] = bool(r == c and np.allclose(A, np.eye(r)))
    info["simetris"] = bool(r == c and np.allclose(A, A.T))
    info["skew_simetris"] = bool(r == c and np.allclose(A, -A.T))
    info["segitiga_atas"] = bool(r == c and np.allclose(A, np.triu(A)))
    info["segitiga_bawah"] = bool(r == c and np.allclose(A, np.tril(A)))
    try:
        info["rank"] = int(np.linalg.matrix_rank(A))
    except Exception:
        info["rank"] = None
    if r == c:
        try:
            det = float(np.linalg.det(A))
            info["determinan"] = det
            info["singular"] = bool(abs(det) < 1e-10)
        except Exception:
            info["determinan"] = None
            info["singular"] = None
        try:
            info["jejak_trace"] = float(np.trace(A))
        except Exception:
            info["jejak_trace"] = None
    return info
