# Intencionalmente defectuosa: sin tipos completos e inconsistente
def suma(a, b):  # sin anotaciones
    return a + b


def division(a, b):  # sin anotaciones; devuelve None a veces
    if b == 0:
        return None  # mypy: retorno inconsistente / Optional no declarado
    return a / b
