import streamlit as st
from backend.combinatoria_y_probabilidad import (
    permutacion_sin_repeticion,
    permutacion_con_repeticion
)


def render():
    """Renderiza la vista de la calculadora de permutaciones."""
    
    # Encabezado principal
    st.header("🔄 Permutaciones")
    
    # Definición y tipos
    st.markdown("""
    **Definición:** Una permutación es un arreglo ordenado de elementos. 
    El orden importa.
    
    **Tipos de permutaciones:**
    - **Sin repetición:** P(n,r) = n!/(n-r)!
    - **Con repetición:** P(n,r) = n^r
    """)
    
    # Selector de tipo de permutación
    tipo_permutacion = st.selectbox(
        "Selecciona el tipo de permutación:",
        ["Sin repetición", "Con repetición"],
        help="Las permutaciones sin repetición no permiten elementos "
             "repetidos, las con repetición sí"
    )
    
    # Layout en dos columnas
    col1, col2 = st.columns([1, 1])
    
    # Columna 1: Calculadora
    with col1:
        st.subheader("Calculadora")
        
        n = st.number_input(
            "n (elementos disponibles)",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            help="Total de elementos diferentes disponibles"
        )
        
        r = st.number_input(
            "r (elementos a seleccionar)",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Número de posiciones a llenar"
        )
        
        if st.button("Calcular Permutaciones", type="primary"):
            try:
                if tipo_permutacion == "Sin repetición":
                    resultado = permutacion_sin_repeticion(n, r)
                    st.success(f"**P({n},{r}) = {resultado:,}**")
                    st.info(
                        f"**Fórmula:** {n}! / ({n}-{r})! = {n}! / "
                        f"{n-r}! = {resultado:,}"
                    )
                    
                    # Ejemplo práctico para casos simples
                    if r <= 3:
                        st.markdown(
                            "**Ejemplo:** Si tienes 5 libros diferentes y "
                            "quieres acomodar 3 en una repisa:"
                        )
                        st.text(
                            "P(5,3) = 5!/(5-3)! = 5!/2! = 120/2 = "
                            "60 formas diferentes"
                        )
                        
                else:  # Con repetición
                    resultado = permutacion_con_repeticion(n, r)
                    st.success(f"**P({n},{r}) = {resultado:,}**")
                    st.info(f"**Fórmula:** {n}^{r} = {resultado:,}")
                    
                    # Ejemplo práctico para casos simples
                    if r <= 3:
                        st.markdown(
                            "**Ejemplo:** Si tienes 5 dígitos (0-9) y "
                            "quieres formar un código de 3 dígitos:"
                        )
                        st.text("P(5,3) = 5³ = 125 códigos posibles")
                        
            except ValueError as e:
                st.error(f"Error: {e}")
    
    # Columna 2: Información adicional
    with col2:
        st.subheader("Información")
        
        # Diferencias clave
        st.markdown("""
        **Diferencias clave:**
        
        **Sin repetición:**
        - Cada elemento solo se puede usar una vez
        - Importa el orden
        - Ejemplo: contraseñas sin dígitos repetidos
        
        **Con repetición:**
        - Los elementos se pueden repetir
        - Importa el orden
        - Ejemplo: códigos PIN
        """)
        
        # Aplicaciones
        st.markdown("""
        **Aplicaciones:**
        - Generación de muestras ordenadas
        - Algoritmos de ordenamiento
        - Análisis de secuencias
        - Modelado de procesos estocásticos
        """)
        
        # Tabla de comparación
        st.markdown("**Ejemplos numéricos:**")
        st.markdown("""
        | n | r | Sin repetición | Con repetición |
        |---|----|----------------|----------------|
        | 3 | 2  | 6              | 9              |
        | 4 | 2  | 12             | 16             |
        | 5 | 3  | 60             | 125            |
        """)