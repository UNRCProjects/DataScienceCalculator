import streamlit as st
from backend.integrales import resolver_integral

def render():
    st.header("🧮 Calculadora de Integrales")
    st.markdown("""
    **Instrucciones:** Ingresa una función y la variable respecto a la cual deseas integrar.
    - Usa la sintaxis de Python (`**` para potencias, `sin(x)` para seno, `exp(x)` para e^x, etc.).
    - Ejemplo: `x**2 + 3*x + sin(x)`
    """)

    expr = st.text_input("Función a integrar:", value="x**2 + 3*x")
    variable = st.text_input("Variable de integración:", value="x")

    if st.button("Resolver integral"):
        resultado = resolver_integral(expr, variable)
        if "Error" in str(resultado):
            st.error(resultado)
        else:
            st.success(f"La integral indefinida de `{expr}` respecto a `{variable}` es:\n\n**{resultado} + C**")
