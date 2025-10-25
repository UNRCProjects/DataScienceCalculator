import streamlit as st
from backend.ecuaciones import resolver_ecuacion_segundo_grado
import math

def render():
    """Renderiza la vista de Ecuaciones de Segundo Grado en Streamlit"""
    st.title("🧮 Solución de Ecuaciones de Segundo Grado")
    st.write("Forma general: ax² + bx + c = 0")

    # Entradas
    a = st.number_input("Coeficiente a", value=1.0, step=0.1)
    b = st.number_input("Coeficiente b", value=0.0, step=0.1)
    c = st.number_input("Coeficiente c", value=0.0, step=0.1)

    # Botón Calcular
    if st.button("Calcular"):
        # Llamar a la función del backend
        resultado = resolver_ecuacion_segundo_grado(a, b, c)

        # Mostrar resultados de forma elegante
        st.subheader("📊 Resultado:")

        if resultado is None:
            st.warning("⚠️ Esto no es una ecuación de segundo grado (a no puede ser 0).")
        elif len(resultado) == 1:
            st.success("✅ Una solución real doble:")
            st.latex(f"x = {resultado[0]:.4f}")
        elif len(resultado) == 2 and isinstance(resultado[0], complex):
            st.info("🔹 Soluciones complejas:")
            x1, x2 = resultado
            st.latex(f"x_1 = {x1.real:.4f} + {x1.imag:.4f}i")
            st.latex(f"x_2 = {x2.real:.4f} - {x2.imag:.4f}i")
        else:
            st.success("✅ Dos soluciones reales distintas:")
            x1, x2 = resultado
            st.latex(f"x_1 = {x1:.4f}")
            st.latex(f"x_2 = {x2:.4f}")
