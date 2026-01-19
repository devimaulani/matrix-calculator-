import numpy as np


def _fmt_matrix(A: np.ndarray) -> str:
    rows = ["[ " + "\t".join(f"{x:8.4g}" for x in row) + " ]" for row in A]
    return "\n".join(rows)


def _fmt_vector(b: np.ndarray) -> str:
    return "[ " + ", ".join(f"{x:.6g}" for x in b.ravel()) + " ]"


def _fmt_aug(A: np.ndarray, b: np.ndarray) -> str:
    A = np.atleast_2d(A.astype(float))
    b = np.atleast_2d(b.astype(float)).reshape(-1, 1)
    parts = []
    for i in range(A.shape[0]):
        left = "\t".join(f"{x:8.4g}" for x in A[i])
        parts.append(f"[ {left} | {b[i,0]:8.4g} ]")
    return "\n".join(parts)


def gaussian_elimination(A: np.ndarray, b: np.ndarray):
    A = A.astype(float).copy()
    b = b.astype(float).copy().reshape(-1, 1)
    m, n = A.shape
    steps = ["Matriks awal [A|b]:", _fmt_aug(A, b)]

    # Forward elimination
    row = 0
    for col in range(n):
        if row >= m:
            break
        # pivot: find max abs in column from row..m-1
        pivot = row + np.argmax(np.abs(A[row:, col]))
        if abs(A[pivot, col]) < 1e-12:
            steps.append(f"Kolom {col} tidak memiliki pivot (semua ~0)")
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
            b[[row, pivot]] = b[[pivot, row]]
            steps.append(f"Tukar baris R{row+1} <-> R{pivot+1}")
            steps.append(_fmt_aug(A, b))
        # Normalize pivot row to 1 (optional for Gauss, helpful for steps)
        piv_val = A[row, col]
        if abs(piv_val - 1.0) > 1e-12:
            A[row] = A[row] / piv_val
            b[row] = b[row] / piv_val
            steps.append(f"Skalakan R{row+1} = R{row+1} / {piv_val:.6g}")
            steps.append(_fmt_aug(A, b))
        # Eliminate rows below
        for r in range(row + 1, m):
            factor = A[r, col]
            if abs(factor) < 1e-12:
                continue
            A[r] = A[r] - factor * A[row]
            b[r] = b[r] - factor * b[row]
            steps.append(f"R{r+1} = R{r+1} - ({factor:.6g})*R{row+1}")
            steps.append(_fmt_aug(A, b))
        row += 1
    try:
        x, *_ = np.linalg.lstsq(A, b, rcond=None)
        x = x.reshape(-1)
        steps.append("Solusi (least squares jika tidak persegi):")
        steps.append(_fmt_vector(x))
        return x, steps
    except Exception as e:
        steps.append(f"Gagal menyelesaikan: {e}")
        raise


def gauss_jordan(A: np.ndarray, b: np.ndarray):
    A = A.astype(float).copy()
    b = b.astype(float).copy().reshape(-1, 1)
    m, n = A.shape
    steps = ["Matriks awal [A|b]:", _fmt_aug(A, b)]

    row = 0
    for col in range(n):
        if row >= m:
            break
        pivot = row + np.argmax(np.abs(A[row:, col]))
        if abs(A[pivot, col]) < 1e-12:
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
            b[[row, pivot]] = b[[pivot, row]]
            steps.append(f"Tukar baris R{row+1} <-> R{pivot+1}")
            steps.append(_fmt_aug(A, b))
        piv_val = A[row, col]
        if abs(piv_val - 1.0) > 1e-12:
            A[row] = A[row] / piv_val
            b[row] = b[row] / piv_val
            steps.append(f"Skalakan R{row+1} = R{row+1} / {piv_val:.6g}")
            steps.append(_fmt_aug(A, b))
        # eliminate above and below
        for r in range(m):
            if r == row:
                continue
            factor = A[r, col]
            if abs(factor) < 1e-12:
                continue
            A[r] = A[r] - factor * A[row]
            b[r] = b[r] - factor * b[row]
            steps.append(f"R{r+1} = R{r+1} - ({factor:.6g})*R{row+1}")
            steps.append(_fmt_aug(A, b))
        row += 1

    try:
        x, *_ = np.linalg.lstsq(A, b, rcond=None)
        x = x.reshape(-1)
        steps.append("Solusi (jika tak tunggal, solusi LS):")
        steps.append(_fmt_vector(x))
        return x, steps
    except Exception as e:
        steps.append(f"Gagal menyelesaikan: {e}")
        raise


def cramer(A: np.ndarray, b: np.ndarray):
    A = A.astype(float)
    b = b.astype(float).reshape(-1)
    n = A.shape[1]
    if A.shape[0] != n:
        raise ValueError("Aturan Cramer memerlukan matriks persegi (n x n)")
    detA = float(np.linalg.det(A))
    steps = [f"det(A) = {detA:.6g}"]
    if abs(detA) < 1e-12:
        steps.append("det(A)=0, tidak ada solusi unik")
        return None, steps
    x = np.zeros(n)
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        detAi = float(np.linalg.det(Ai))
        xi = detAi / detA
        x[i] = xi
        steps.append(f"det(A_{i+1}) = {detAi:.6g} -> x{i+1} = det(A_{i+1})/det(A) = {xi:.6g}")
    steps.append("Solusi:")
    steps.append(_fmt_vector(x))
    return x, steps


def inverse_method(A: np.ndarray, b: np.ndarray):
    A = A.astype(float)
    b = b.astype(float).reshape(-1)
    if A.shape[0] != A.shape[1]:
        raise ValueError("Metode invers memerlukan A persegi (n x n)")
    detA = float(np.linalg.det(A))
    if abs(detA) < 1e-12:
        raise ValueError("Matriks A singular, tidak memiliki invers")
    Ainv = np.linalg.inv(A)
    x = Ainv @ b
    steps = [
        f"det(A) = {detA:.6g}",
        "A^{-1}:",
        _fmt_matrix(Ainv),
        "x = A^{-1} b:",
        _fmt_vector(x),
    ]
    return x, steps
