from __future__ import annotations


def suma(a: float, b: float) -> float:
    """Suma dos números (float|int) y retorna float."""
    return float(a) + float(b)


def division(a: float, b: float) -> float:
    """Divide a entre b. Lanza ValueError si b == 0."""
    if b == 0:
        raise ValueError("La división por cero no está permitida.")
    return float(a) / float(b)
