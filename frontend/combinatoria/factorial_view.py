import streamlit as st
from backend.combinatoria_y_probabilidad import factorial


def render():
    """Renderiza la vista de la calculadora de factorial."""
    
    # Encabezado principal
    st.header("📊 Factorial")
    
    # Definición y fórmula
    st.markdown("""
    **Definición:** El factorial de un número n (n!) es el producto de todos 
    los enteros positivos desde 1 hasta n. Por definición, 0! = 1.
    
    **Fórmula:** n! = n × (n-1) × (n-2) × ... × 2 × 1
    
    **Ejemplos:**
    - 5! = 5 × 4 × 3 × 2 × 1 = 120
    - 3! = 3 × 2 × 1 = 6
    - 0! = 1
    """)
    
    # Layout en dos columnas
    col1, col2 = st.columns([1, 1])
    
    # Columna 1: Calculadora
    with col1:
        st.subheader("Calculadora")
        
        n = st.number_input(
            "Número n",
            min_value=0,
            max_value=20,
            value=5,
            step=1,
            help="Máximo 20 para evitar números muy grandes"
        )
        
        if st.button("Calcular Factorial", type="primary"):
            try:
                resultado = factorial(n)
                st.success(f"**{n}! = {resultado:,}**")
                
                # Mostrar descomposición si n > 0
                if n > 0:
                    descomposicion = " × ".join(
                        str(i) for i in range(n, 0, -1)
                    )
                    st.info(f"**Descomposición:** {descomposicion}")
                    
            except ValueError as e:
                st.error(f"Error: {e}")
    
    # Columna 2: Información adicional
    with col2:
        st.subheader("Información")
        
        st.markdown("""
        **Aplicaciones:**
        - Cálculo de permutaciones y combinaciones
        - Distribuciones de probabilidad
        - Análisis combinatorio
        - Algoritmos de ordenamiento
        """)
        
        # Tabla de factoriales conocidos
        st.markdown("**Factoriales conocidos:**")
        
        factoriales_conocidos = {
            0: 1,
            1: 1,
            2: 2,
            3: 6,
            4: 24,
            5: 120,
            6: 720,
            7: 5040,
            8: 40320,
            9: 362880,
            10: 3628800
        }
        
        for num, fact in factoriales_conocidos.items():
            st.text(f"{num}! = {fact:,}")