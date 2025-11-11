from sympy import symbols, integrate, sympify

def resolver_integral(expr_str, variable_str):
    try:
        var = symbols(variable_str)
        expr = sympify(expr_str)
        resultado = integrate(expr, var)
        return resultado
    except Exception as e:
        return f"Error: {str(e)}"
