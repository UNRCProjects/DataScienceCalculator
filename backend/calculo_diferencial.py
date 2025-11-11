import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

def derivar_funcion(funcion_str: str):
    """Recibe la función ingresada como string y retorna la función sympy y su derivada, ambos en formato sympy."""
    x = sp.symbols('x')
    # --- Preprocesamiento de texto ---
    func_str_processed = funcion_str.lower()
    # Potencias con ^ → **
    func_str_processed = func_str_processed.replace('^', '**')
    # Funciones trigonométricas y logarítmicas
    func_str_processed = func_str_processed.replace('sen', 'sin')
    func_str_processed = func_str_processed.replace('tg', 'tan')
    func_str_processed = func_str_processed.replace('ln', 'log')
    func_str_processed = func_str_processed.replace('log10', 'log(x,10)')
    # Raíz cuadrada (raiz(x) o √x)
    func_str_processed = func_str_processed.replace('raiz', 'sqrt')
    func_str_processed = func_str_processed.replace('√', 'sqrt')
    # Valor absoluto con barras o abs().
    func_str_processed = func_str_processed.replace('|', 'Abs(') if '|' in func_str_processed else func_str_processed
    if func_str_processed.count('Abs(') % 2 != 0:
        func_str_processed += ')'
    # Transformaciones: multiplicación implícita (4x → 4*x)
    transformations = standard_transformations + (implicit_multiplication_application,)
    # Parseo seguro
    funcion_sympy = parse_expr(func_str_processed, transformations=transformations, local_dict={'x': x})
    # Calcular derivada
    derivada = sp.diff(funcion_sympy, x)
    return funcion_sympy, derivada
