import sympy as sp 
import streamlit as st
from backend.calculo_diferencial import derivar_funcion

def render():
    st.title("Derivadas")
    st.markdown(
    """
    La derivada de una función es una herramienta matemática que permite conocer cómo varía el valor de esa función cuando cambia su variable independiente, es decir, indica la **velocidad de cambio instantánea** de la función en cada punto.
    \n
    En términos geométricos, representa la pendiente de la recta tangente a la gráfica de la función en un punto específico.
    \n
    La definición formal de la derivada de una función f(x) es:
    \n
    """
    )
    st.latex(r'''f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}''')
    st.subheader("Calculadora de Derivadas")
    st.markdown("""
    Ejemplos de funciones válidos:
    - `x^2 - 4x + 5`
    - `3sen(x)`
    - `raiz(x) + 2x^3`
    - `|x| + log10(x)`
    """, unsafe_allow_html=True)

    funcion_str = st.text_input("Introduce la función f(x):", "x^2-4x-5")

    if st.button("Calcular Derivada"):
        try:
            funcion_sympy, derivada = derivar_funcion(funcion_str)
            st.success(f"La derivada de f(x) = {sp.pretty(funcion_sympy)} es:")
            st.latex(f"f'(x) = {sp.latex(derivada)}")
        except Exception as e:
            st.error(f"❌ Error al procesar la función. Verifica la sintaxis. Detalle: {e}")
