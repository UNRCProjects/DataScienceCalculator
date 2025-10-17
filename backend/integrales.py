from sympy import symbols, integrate, sympify

def resolver_integral(expr_str, variable_str):
    """
    Resuelve una integral simbólica con sympy.
    :param expr_str: expresión a integrar, en formato string (ej. "x**2 + 3*x")
    :param variable_str: variable de integración, en formato string (ej. "x")
    :return: resultado simbólico de la integral
    """
    try:
        var = symbols(variable_str)
        expr = sympify(expr_str)
        resultado = integrate(expr, var)
        return resultado
    except Exception as e:
        return f"Error: {str(e)}"
