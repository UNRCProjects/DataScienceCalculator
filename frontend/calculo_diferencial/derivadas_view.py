import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

def render():
    st.title("Cálculo Diferencial - Derivadas")
    
    st.markdown(
        """
    La **derivada de una función** es una herramienta matemática que permite conocer cómo varía el valor de esa función cuando cambia su variable independiente.  
    Es decir, indica la **velocidad de cambio instantánea** de la función en cada punto.  
    En términos geométricos, representa la **pendiente de la recta tangente** a la gráfica de la función en un punto específico.

    La definición formal de la derivada de una función f(x) es:
    """
    )
    st.latex(r'''f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}''')

    st.subheader("📘 Calculadora de Derivadas")
    
    st.markdown("""
    Escribe una función y presiona **Calcular Derivada**.  
    Ejemplos válidos:
    - `x^2 - 4x + 5`
    - `3sen(x)`
    - `raiz(x) + 2x^3`
    - `|x| + log10(x)`
    """, unsafe_allow_html=True)

    funcion_str = st.text_input("Introduce la función f(x):", "x^2-4x-5")

    if st.button("Calcular Derivada"):
        try:
            x = sp.symbols('x')

            # --- Preprocesamiento de texto ---
            func_str_processed = funcion_str.lower()

            # Potencias con ^ → **
            func_str_processed = func_str_processed.replace('^', '**')

            # Funciones trigonométricas y logarítmicas
            func_str_processed = func_str_processed.replace('sen', 'sin')
            func_str_processed = func_str_processed.replace('tg', 'tan')
            func_str_processed = func_str_processed.replace('ln', 'log')  # por si escriben ln(x)
            func_str_processed = func_str_processed.replace('log10', 'log(x,10)')
            
            # Raíz cuadrada (raiz(x) o √x)
            func_str_processed = func_str_processed.replace('raiz', 'sqrt')
            func_str_processed = func_str_processed.replace('√', 'sqrt')

            # Valor absoluto con barras o abs()
            func_str_processed = func_str_processed.replace('|', 'Abs(') if '|' in func_str_processed else func_str_processed
            if func_str_processed.count('Abs(') % 2 != 0:
                func_str_processed += ')'  # cierra si falta paréntesis de cierre

            # Transformaciones: multiplicación implícita (4x → 4*x)
            transformations = standard_transformations + (implicit_multiplication_application,)

            # Parseo seguro
            funcion_sympy = parse_expr(func_str_processed, transformations=transformations, local_dict={'x': x})

            # Calcular derivada
            derivada = sp.diff(funcion_sympy, x)

            # Mostrar resultados
            st.success(f"La derivada de f(x) = {sp.pretty(funcion_sympy)} es:")
            st.latex(f"f'(x) = {sp.latex(derivada)}")

        except Exception as e:
            st.error(f"❌ Error al procesar la función. Verifica la sintaxis. Detalle: {e}")
