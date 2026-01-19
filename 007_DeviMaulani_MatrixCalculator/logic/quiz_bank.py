import random
from typing import Dict, List
import numpy as np

# Difficulty: 'Easy' | 'Medium' | 'Hard'


def _fmt_matrix(A: np.ndarray) -> str:
    rows = ["[ " + ", ".join(f"{float(x):.0f}" for x in row) + " ]" for row in A]
    return "\n".join(rows)


def _choice_explanations(correct_text: str, steps: List[str]) -> str:
    return "\n".join([correct_text, "", "Penjelasan:"] + steps)


def q_matrix_addition(level: str) -> Dict:
    r = 2 if level == 'Easy' else (2 if level == 'Medium' else 3)
    c = 2 if level == 'Easy' else (3 if level == 'Medium' else 3)
    A = np.random.randint(-5, 6, size=(r, c))
    B = np.random.randint(-5, 6, size=(r, c))
    C = A + B
    correct = _fmt_matrix(C)
    # wrong options: small perturbations
    opt2 = _fmt_matrix(C + np.eye(r, c))
    opt3 = _fmt_matrix(A - B)  # subtraction instead of addition
    prompt = f"Jika A dan B seperti berikut, berapakah A + B?\n\nA =\n{_fmt_matrix(A)}\n\nB =\n{_fmt_matrix(B)}"
    expl = _choice_explanations("A + B dihitung elemen per elemen", [
        "C[i,j] = A[i,j] + B[i,j]",
        "Hasilnya ditulis seperti pada pilihan yang benar."
    ])
    options = [correct, opt2, opt3]
    random.shuffle(options)
    correct_index = options.index(correct)
    return {
        'category': 'Matrix',
        'prompt': prompt,
        'options': options,
        'correct_index': correct_index,
        'explanation': expl,
        'score': 10,
    }


def q_det(level: str) -> Dict:
    if level == 'Easy':
        A = np.random.randint(-4, 5, size=(2, 2))
        det = float(np.linalg.det(A))
        prompt = f"Hitung det(A) untuk matriks 2x2 berikut:\n\nA =\n{_fmt_matrix(A)}"
        expl = _choice_explanations("determinannya adalah ad - bc", [
            f"det(A) = {A[0,0]}*{A[1,1]} - {A[0,1]}*{A[1,0]} = {det:.0f}"
        ])
    else:
        A = np.random.randint(-3, 4, size=(3, 3))
        det = float(np.linalg.det(A))
        prompt = f"Hitung det(A) untuk matriks 3x3 berikut:\n\nA =\n{_fmt_matrix(A)}"
        expl = _choice_explanations("gunakan aturan Sarrus atau ekspansi kofaktor", [
            f"det(A) ≈ {det:.0f} (hasil tepat pada pilihan yang benar)"
        ])
    correct = f"{det:.0f}"
    wrong1 = f"{det + random.choice([-2, -1, 1, 2]):.0f}"
    wrong2 = f"{det * random.choice([2, -1]):.0f}"
    options = [correct, wrong1, wrong2]
    random.shuffle(options)
    correct_index = options.index(correct)
    return {
        'category': 'Matrix',
        'prompt': prompt,
        'options': options,
        'correct_index': correct_index,
        'explanation': expl,
        'score': 15 if level == 'Hard' else 12,
    }


def q_dot(level: str) -> Dict:
    n = 2 if level == 'Easy' else 3
    v1 = np.random.randint(-5, 6, size=(n,))
    v2 = np.random.randint(-5, 6, size=(n,))
    val = int(np.dot(v1, v2))
    prompt = f"Hitung dot product v·w.\n\nv = {_fmt_matrix(v1.reshape(-1,1))}\n\nw = {_fmt_matrix(v2.reshape(-1,1))}"
    expl = _choice_explanations("v·w = Σ v_i w_i", [
        "Kalikan pasangan elemen lalu jumlahkan."
    ])
    correct = f"{val}"
    wrong1 = f"{val + random.choice([-3,-2,-1,1,2,3])}"
    wrong2 = f"{val * random.choice([2,-1])}"
    options = [correct, wrong1, wrong2]
    random.shuffle(options)
    correct_index = options.index(correct)
    return {
        'category': 'Vector',
        'prompt': prompt,
        'options': options,
        'correct_index': correct_index,
        'explanation': expl,
        'score': 10,
    }


def q_cross(level: str) -> Dict:
    v1 = np.random.randint(-3, 4, size=(3,))
    v2 = np.random.randint(-3, 4, size=(3,))
    c = np.cross(v1, v2)
    prompt = f"Hitung v × w untuk vektor 3D berikut.\n\nv = {_fmt_matrix(v1.reshape(-1,1))}\n\nw = {_fmt_matrix(v2.reshape(-1,1))}"
    correct = f"{_fmt_matrix(c.reshape(-1,1))}"
    wrong1 = f"{_fmt_matrix((-c).reshape(-1,1))}"
    wrong2 = f"{_fmt_matrix(np.array([c[1], c[2], c[0]]).reshape(-1,1))}"
    expl = _choice_explanations("Gunakan determinan i, j, k atau aturan silang komponen", [
        "i*(v2*w3 - v3*w2) - j*(v1*w3 - v3*w1) + k*(v1*w2 - v2*w1)"
    ])
    options = [correct, wrong1, wrong2]
    random.shuffle(options)
    correct_index = options.index(correct)
    return {
        'category': 'Vector',
        'prompt': prompt,
        'options': options,
        'correct_index': correct_index,
        'explanation': expl,
        'score': 15 if level != 'Easy' else 12,
    }


def q_spl(level: str) -> Dict:
    n = 2 if level == 'Easy' else (2 if level == 'Medium' else 3)
    while True:
        A = np.random.randint(-4, 5, size=(n, n))
        if abs(np.linalg.det(A)) > 1e-6:
            break
    x_true = np.random.randint(-3, 4, size=(n,))
    b = A @ x_true
    prompt = f"Selesaikan Ax = b untuk x.\n\nA =\n{_fmt_matrix(A)}\n\nb =\n{_fmt_matrix(b.reshape(-1,1))}"
    correct = _fmt_matrix(x_true.reshape(-1,1))
    wrong1 = _fmt_matrix((x_true + 1).reshape(-1,1))
    wrong2 = _fmt_matrix((x_true * -1).reshape(-1,1))
    expl = _choice_explanations("Gunakan eliminasi Gauss atau invers", [
        "Rujuk langkah: eliminasi ke bentuk segitiga, substitusi balik."
    ])
    options = [correct, wrong1, wrong2]
    random.shuffle(options)
    correct_index = options.index(correct)
    return {
        'category': 'SPL',
        'prompt': prompt,
        'options': options,
        'correct_index': correct_index,
        'explanation': expl,
        'score': 15 if level == 'Hard' else 12,
    }


def get_random_question(level: str) -> Dict:
    pool = []
    if level == 'Easy':
        pool = [q_matrix_addition, q_det, q_dot, q_spl]
    elif level == 'Medium':
        pool = [q_matrix_addition, q_det, q_dot, q_cross, q_spl]
    else:
        pool = [q_matrix_addition, q_det, q_cross, q_spl]
    q_fn = random.choice(pool)
    return q_fn(level)
