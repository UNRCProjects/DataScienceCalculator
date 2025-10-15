import streamlit as st
from backend.combinatoria_y_probabilidad import combinacion


def render():
    """Renderiza la vista de la calculadora de combinaciones."""
    
    # Encabezado principal
    st.header("🎯 Combinaciones")
    
    # Definición y fórmula
    st.markdown("""
    **Definición:** Una combinación es una selección no ordenada de elementos. 
    El orden NO importa.
    
    **Fórmula:** C(n,r) = n! / (r! × (n-r)!) = (n r)
    
    También conocido como coeficiente binomial.
    """)
    
    # Layout en dos columnas
    col1, col2 = st.columns([1, 1])
    
    # Columna 1: Calculadora
    with col1:
        st.subheader("Calculadora")
        
        n = st.number_input(
            "n (elementos disponibles)",
            min_value=1,
            max_value=20,
            value=10,
            step=1,
            help="Total de elementos diferentes disponibles"
        )
        
        r = st.number_input(
            "r (elementos a seleccionar)",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Número de elementos a seleccionar"
        )
        
        if st.button("Calcular Combinaciones", type="primary"):
            try:
                resultado = combinacion(n, r)
                st.success(f"**C({n},{r}) = {resultado:,}**")
                st.info(
                    f"**Fórmula:** {n}! / ({r}! × ({n}-{r})!) = {resultado:,}"
                )
                
                # Ejemplo práctico para casos simples
                if r <= 5:
                    st.markdown(
                        "**Ejemplo:** Si tienes 10 estudiantes y quieres "
                        "formar un comité de 3:"
                    )
                    st.text("C(10,3) = 10!/(3!×7!) = 120 formas diferentes")
                    st.text(
                        "(El orden no importa: Juan, María, Pedro = "
                        "Pedro, María, Juan)"
                    )
                
                # Mostrar propiedades matemáticas
                if r <= n:
                    st.markdown("**Propiedades:**")
                    complemento = combinacion(n, n - r)
                    st.text(f"• C({n},{r}) = C({n},{n-r}) = {complemento:,}")
                    
                    if r > 0:
                        st.text(
                            f"• C({n},{r}) = C({n-1},{r-1}) + C({n-1},{r})"
                        )
                        
            except ValueError as e:
                st.error(f"Error: {e}")
    
    # Columna 2: Información adicional
    with col2:
        st.subheader("Información")
        
        # Diferencias con permutaciones
        st.markdown("""
        **Diferencias con Permutaciones:**
        
        **Permutaciones:** ABC ≠ ACB (orden importa)
        **Combinaciones:** {A,B,C} = {C,A,B} (orden no importa)
        
        **Relación:** P(n,r) = C(n,r) × r!
        """)
        
        # Aplicaciones
        st.markdown("""
        **Aplicaciones:**
        - Selección de muestras aleatorias
        - Análisis combinatorio
        - Algoritmos de optimización
        - Teoría de grafos
        - Análisis de características
        """)
        
        # Triángulo de Pascal
        st.markdown("**Triángulo de Pascal (coeficientes binomiales):**")
        
        pascal_triangle = [
            [1],
            [1, 1],
            [1, 2, 1],
            [1, 3, 3, 1],
            [1, 4, 6, 4, 1],
            [1, 5, 10, 10, 5, 1]
        ]
        
        for i, row in enumerate(pascal_triangle):
            espacios = " " * (6 - i)
            numeros = " ".join(f"{num:2d}" for num in row)
            st.text(espacios + numeros)
        
        # Ejemplos numéricos comunes
        st.markdown("**Ejemplos comunes:**")
        st.markdown("""
        | Situación | n | r | C(n,r) |
        |-----------|---|----|--------|
        | Lotería (6 de 49) | 49 | 6 | 13,983,816 |
        | Comité (5 de 20) | 20 | 5 | 15,504 |
        | Equipo (11 de 22) | 22 | 11 | 646,646 |
        """)