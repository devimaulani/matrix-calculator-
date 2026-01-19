import numpy as np
from math import acos, degrees


def add(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    if u.shape != v.shape:
        raise ValueError(f"Dimensi vektor harus sama: {u.shape} vs {v.shape}")
    return u + v


def sub(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    if u.shape != v.shape:
        raise ValueError(f"Dimensi vektor harus sama: {u.shape} vs {v.shape}")
    return u - v


def lincomb(alpha: float, u: np.ndarray, beta: float, v: np.ndarray) -> np.ndarray:
    if u.shape != v.shape:
        raise ValueError(f"Dimensi vektor harus sama: {u.shape} vs {v.shape}")
    return alpha * u + beta * v


def dot(u: np.ndarray, v: np.ndarray) -> float:
    if u.shape != v.shape:
        raise ValueError(f"Dimensi vektor harus sama: {u.shape} vs {v.shape}")
    return float(np.dot(u, v))


def cross(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    if u.shape[0] != 3 or v.shape[0] != 3:
        raise ValueError("Cross product hanya didefinisikan untuk vektor 3D")
    return np.cross(u, v)


def norm(u: np.ndarray) -> float:
    return float(np.linalg.norm(u))


def projection_u_on_v(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    den = float(np.dot(v, v))
    if abs(den) < 1e-12:
        raise ValueError("Vektor v adalah nol, tidak dapat memproyeksikan")
    scalar = float(np.dot(u, v) / den)
    return scalar * v


def angle_between(u: np.ndarray, v: np.ndarray) -> float:
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    if nu < 1e-12 or nv < 1e-12:
        raise ValueError("Sudut tidak terdefinisi untuk vektor nol")
    cos_th = float(np.clip(np.dot(u, v) / (nu * nv), -1.0, 1.0))
    return float(degrees(acos(cos_th)))
