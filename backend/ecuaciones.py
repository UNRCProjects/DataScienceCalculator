import math

def resolver_ecuacion_segundo_grado(a, b, c):
    """
    Resuelve una ecuación cuadrática de la forma ax² + bx + c = 0
    Parámetros:
        a (float): coeficiente cuadrático
        b (float): coeficiente lineal
        c (float): término independiente
    """
    print("=== Solución de ecuaciones de segundo grado ===")
    print("Forma general: ax² + bx + c = 0\n")

    if a == 0:
        print("\n⚠️ Esto no es una ecuación de segundo grado (a no puede ser 0).")
        return None
    else:
        discriminante = b**2 - 4*a*c
        print(f"\nDiscriminante (b² - 4ac) = {discriminante}")

        if discriminante > 0:
            x1 = (-b + math.sqrt(discriminante)) / (2*a)
            x2 = (-b - math.sqrt(discriminante)) / (2*a)
            print(f"\n✅ Dos soluciones reales:")
            print(f"x₁ = {x1}")
            print(f"x₂ = {x2}")
            return (x1, x2)

        elif discriminante == 0:
            x = -b / (2*a)
            print(f"\n✅ Una solución real doble:")
            print(f"x = {x}")
            return (x,)

        else:
            real = -b / (2*a)
            imaginaria = math.sqrt(abs(discriminante)) / (2*a)
            print(f"\n🔹 Soluciones complejas:")
            print(f"x₁ = {real} + {imaginaria}i")
            print(f"x₂ = {real} - {imaginaria}i")
            return (complex(real, imaginaria), complex(real, -imaginaria))


# 👇 Este bloque solo se ejecuta si ejecutas ecuaciones.py directamente
if __name__ == "__main__":
    a = float(input("Ingresa el valor de a: "))
    b = float(input("Ingresa el valor de b: "))
    c = float(input("Ingresa el valor de c: "))

    resolver_ecuacion_segundo_grado(a, b, c)
    print("\n¡Gracias por usar el solucionador de ecuaciones de segundo grado!")
