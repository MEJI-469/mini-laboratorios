# mini-laboratorios/labs/lab1/main.py
"""
Laboratorio 1
Módulo A — Funciones y Métodos
Módulo B — Excepciones
Módulo C — Decoradores

Ejecuta: python labs/lab1/main.py
"""

from __future__ import annotations
from functools import wraps
from typing import Any, Callable, Iterable, Tuple, List, Dict


# =========================
# MÓDULO A — FUNCIONES Y MÉTODOS
# =========================
# A.1 – Funciones como valores + *args y **kwargs


def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"


def despedir(nombre: str) -> str:
    return f"Adiós, {nombre}"


def aplaudir(nombre: str, veces: int = 3, emoji: str = "👏") -> str:
    return f"{nombre}: " + (emoji * veces)


# Diccionario que mapea nombres a funciones (funciones como valores)
acciones: Dict[str, Callable[..., Any]] = {
    "saludar": saludar,
    "despedir": despedir,
    "aplaudir": aplaudir,
}


def ejecutar(accion: str, *args, **kwargs) -> Any:
    """
    Busca la función por nombre en 'acciones' y la ejecuta con *args/**kwargs.
    Lanza ValueError si la acción no existe.
    """
    try:
        funcion = acciones[accion]
    except KeyError:
        disponibles = ", ".join(sorted(acciones.keys()))
        raise ValueError(f"Acción desconocida: '{accion}'. Opciones: {disponibles}")
    return funcion(*args, **kwargs)


# A.2 – Funciones internas y closures


def crear_descuento(porcentaje: float) -> Callable[[float], float]:
    """
    Devuelve una función que aplica el descuento 'porcentaje' (por ejemplo 0.10 = 10%)
    sobre un precio recibido.
    """

    def aplicar(precio: float) -> float:
        return round(precio * (1 - porcentaje), 2)

    return aplicar


# =========================
# MÓDULO B — EXCEPCIONES
# =========================
# B.1 – Validación de entrada (sin I/O de archivos)


def parsear_enteros(entradas: List[str]) -> Tuple[List[int], List[str]]:
    """
    Convierte cada string a entero. Si alguno falla, registra un mensaje de error.
    Retorna (valores_convertidos, mensajes_error).
    El proceso continúa aunque haya errores.
    """
    valores: List[int] = []
    errores: List[str] = []
    for i, s in enumerate(entradas):
        try:
            valores.append(int(s))
        except ValueError:
            errores.append(f"Entrada inválida en índice {i}: '{s}' no es un entero")
    return valores, errores


# B.2 – Excepciones personalizadas y raise


class CantidadInvalida(Exception):
    """Se lanza cuando la cantidad es menor o igual a 0."""

    pass


def calcular_total(precio_unitario: float, cantidad: int) -> float:
    """
    - Lanza CantidadInvalida si cantidad <= 0
    - Lanza ValueError si precio_unitario < 0
    - Devuelve precio_unitario * cantidad en caso válido
    """
    if cantidad <= 0:
        raise CantidadInvalida(f"La cantidad debe ser > 0. Recibido: {cantidad}")
    if precio_unitario < 0:
        raise ValueError(f"El precio unitario no puede ser negativo. Recibido: {precio_unitario}")
    return precio_unitario * cantidad


# =========================
# MÓDULO C — DECORADORES
# =========================
# C.1 – Decorador de validación


def requiere_positivos(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Verifica que todos los argumentos numéricos (posicionales y nombrados)
    sean > 0; si no, lanza ValueError con un mensaje útil.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        def es_numero(x: Any) -> bool:
            return isinstance(x, (int, float)) and not isinstance(x, bool)

        # Revisar *args
        for idx, a in enumerate(args):
            if es_numero(a) and a <= 0:
                raise ValueError(
                    f"Argumento posicional #{idx + 1} de '{func.__name__}' debe ser > 0. Recibido: {a}"
                )

        # Revisar **kwargs
        for k, v in kwargs.items():
            if es_numero(v) and v <= 0:
                raise ValueError(
                    f"Argumento '{k}' de '{func.__name__}' debe ser > 0. Recibido: {v}"
                )

        return func(*args, **kwargs)

    return wrapper


@requiere_positivos
def calcular_descuento(precio: float, porcentaje: float) -> float:
    """
    Aplica un descuento (por ejemplo 0.2 = 20%) a 'precio'.
    Requiere que ambos sean positivos (> 0).
    """
    return round(precio * (1 - porcentaje), 2)


@requiere_positivos
def escala(valor: float, factor: float) -> float:
    """Multiplica 'valor' por 'factor'. Ambos deben ser > 0."""
    return valor * factor


# =========================
# DEMOS / AUTOPRUEBAS SENCILLAS
# =========================


def _demo_modulo_a():
    print("\n=== Módulo A ===")

    # A.1
    print("A.1 – ejecutar('saludar', 'Ana'):")
    res = ejecutar("saludar", "Ana")
    print(" ->", res)
    assert res == "Hola, Ana"

    print("A.1 – ejecutar('aplaudir', 'Marlon', veces=4):")
    res = ejecutar("aplaudir", "Marlon", veces=4)
    print(" ->", res)

    # Acción inexistente
    try:
        ejecutar("no-existe", "X")
    except ValueError as e:
        print("Acción inexistente OK ->", e)

    # A.2
    print("\nA.2 – closures de descuento:")
    descuento10 = crear_descuento(0.10)
    descuento25 = crear_descuento(0.25)
    print("descuento10(100) ->", descuento10(100))
    print("descuento25(80)  ->", descuento25(80))
    assert descuento10(100) == 90.0
    assert descuento25(80) == 60.0


def _demo_modulo_b():
    print("\n=== Módulo B ===")

    # B.1
    entradas = ["10", "x", "3"]
    valores, errores = parsear_enteros(entradas)
    print("parsear_enteros(['10', 'x', '3']) ->", valores, "| errores:", errores)
    assert valores == [10, 3]
    assert any("x" in e for e in errores)

    # B.2
    print("\nB.2 – calcular_total(10, 3) ->", calcular_total(10, 3))
    assert calcular_total(10, 3) == 30

    try:
        calcular_total(10, 0)
    except CantidadInvalida as e:
        print("CantidadInvalida OK ->", e)

    try:
        calcular_total(-1, 2)
    except ValueError as e:
        print("ValueError (precio negativo) OK ->", e)


def _demo_modulo_c():
    print("\n=== Módulo C ===")

    print("calcular_descuento(100, 0.2) ->", calcular_descuento(100, 0.2))
    assert calcular_descuento(100, 0.2) == 80.0

    try:
        calcular_descuento(-1, 0.2)
    except ValueError as e:
        print("ValueError por argumento no positivo OK ->", e)

    print("escala(5, 2) ->", escala(5, 2))
    assert escala(5, 2) == 10

    try:
        escala(5, 0)
    except ValueError as e:
        print("ValueError por factor no positivo OK ->", e)


def main():
    _demo_modulo_a()
    _demo_modulo_b()
    _demo_modulo_c()
    print("\n✅ Todas las verificaciones básicas del Lab 1 pasaron.")


if __name__ == "__main__":
    main()
