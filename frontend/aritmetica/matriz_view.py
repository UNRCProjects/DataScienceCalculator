import streamlit as st
from backend.matriz import multiplicar_matrices

def render():
    st.header("Multiplicación de Matrices")
    st.markdown("""
    **Instrucciones:**
    - Define el tamaño de las matrices A y B.
    - Ingresa los valores separados por comas en cada fila.
    - Ejemplo de una fila: `1, 2, 3`
    """)

    # Dimensiones
    col1, col2 = st.columns(2)
    with col1:
        filas_A = st.number_input("Filas de A", min_value=1, value=2)
        columnas_A = st.number_input("Columnas de A", min_value=1, value=2)
    with col2:
        filas_B = st.number_input("Filas de B", min_value=1, value=2)
        columnas_B = st.number_input("Columnas de B", min_value=1, value=2)

    # Validar compatibilidad
    if columnas_A != filas_B:
        st.warning("Las columnas de A deben ser iguales a las filas de B para poder multiplicarlas.")

    # Ingreso de datos para matriz A
    st.subheader("Matriz A")
    matriz_A = []
    for i in range(int(filas_A)):
        fila_str = st.text_input(f"Fila {i+1} de A (valores separados por comas):", key=f"A_{i}")
        if fila_str:
            try:
                fila = [float(x.strip()) for x in fila_str.split(",")]
                if len(fila) != columnas_A:
                    st.error(f"La fila {i+1} debe tener {columnas_A} elementos.")
                matriz_A.append(fila)
            except ValueError:
                st.error(f"Error: La fila {i+1} contiene valores no numéricos.")

    # Ingreso de datos para matriz B
    st.subheader("Matriz B")
    matriz_B = []
    for i in range(int(filas_B)):
        fila_str = st.text_input(f"Fila {i+1} de B (valores separados por comas):", key=f"B_{i}")
        if fila_str:
            try:
                fila = [float(x.strip()) for x in fila_str.split(",")]
                if len(fila) != columnas_B:
                    st.error(f"La fila {i+1} debe tener {columnas_B} elementos.")
                matriz_B.append(fila)
            except ValueError:
                st.error(f"Error: La fila {i+1} contiene valores no numéricos.")

    # Botón de cálculo
    if st.button("Calcular A x B"):
        if len(matriz_A) == filas_A and len(matriz_B) == filas_B:
            resultado = multiplicar_matrices(matriz_A, matriz_B)
            if resultado is None:
                st.error("No se pueden multiplicar las matrices: columnas de A ≠ filas de B")
            elif isinstance(resultado, str) and "Error" in resultado:
                st.error(resultado)
            else:
                st.success("Resultado de A x B:")
                for fila in resultado:
                    st.write(fila)
        else:
            st.warning("Por favor, ingresa todas las filas de ambas matrices antes de calcular.")
