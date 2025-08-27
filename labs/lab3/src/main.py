from __future__ import annotations

from operaciones import suma, division


def demo():
    print("=== Demo Lab 3: operaciones ===")
    print("suma(10, 5) ->", suma(10, 5))

    try:
        print("division(10, 2) ->", division(10, 2))
        print("division(10, 0) -> (debe fallar)")
        print(division(10, 0))  # caso límite: dispara ValueError
    except ValueError as e:
        print("OK, error controlado:", e)


def main():
    demo()
    print("\n✅ Lab 3 ejecutado correctamente desde main.py")


if __name__ == "__main__":
    main()
