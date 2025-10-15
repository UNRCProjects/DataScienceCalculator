import streamlit as st
from backend.combinatoria_y_probabilidad import (
    probabilidad_evento_simple,
    probabilidad_complemento,
    probabilidad_union_eventos_independientes
)


def render():
    """Renderiza la vista de la calculadora de probabilidad básica."""
    
    # Encabezado principal
    st.header("🎲 Probabilidad Básica")
    
    # Definición y fórmula básica
    st.markdown("""
    **Definición:** La probabilidad mide la posibilidad de que ocurra un evento.
    
    **Fórmula básica:** P(A) = casos_favorables / casos_posibles
    """)
    
    # Selector de tipo de cálculo
    tipo_calculo = st.selectbox(
        "Selecciona el tipo de cálculo:",
        [
            "Probabilidad simple",
            "Evento complementario",
            "Unión de eventos independientes"
        ],
        help="Diferentes tipos de cálculos probabilísticos"
    )
    
    # Layout en dos columnas
    col1, col2 = st.columns([1, 1])
    
    # Columna 1: Calculadora
    with col1:
        st.subheader("Calculadora")
        
        if tipo_calculo == "Probabilidad simple":
            st.markdown("**Probabilidad de un evento simple**")
            
            casos_favorables = st.number_input(
                "Casos favorables",
                min_value=0,
                value=3,
                step=1,
                help="Número de resultados que favorecen el evento"
            )
            
            casos_posibles = st.number_input(
                "Casos posibles",
                min_value=1,
                value=10,
                step=1,
                help="Número total de resultados posibles"
            )
            
            if st.button("Calcular Probabilidad", type="primary"):
                try:
                    resultado = probabilidad_evento_simple(
                        casos_favorables,
                        casos_posibles
                    )
                    porcentaje = resultado * 100
                    
                    st.success(f"**P(A) = {resultado:.4f}**")
                    st.success(f"**Porcentaje = {porcentaje:.2f}%**")
                    st.info(
                        f"**Fórmula:** {casos_favorables} / "
                        f"{casos_posibles} = {resultado:.4f}"
                    )
                    
                    # Interpretación cualitativa
                    if resultado == 0:
                        interpretacion = "Imposible"
                    elif resultado < 0.1:
                        interpretacion = "Muy poco probable"
                    elif resultado < 0.3:
                        interpretacion = "Poco probable"
                    elif resultado < 0.7:
                        interpretacion = "Probabilidad moderada"
                    elif resultado < 0.9:
                        interpretacion = "Muy probable"
                    else:
                        interpretacion = "Casi seguro"
                    
                    st.info(f"**Interpretación:** {interpretacion}")
                    
                except ValueError as e:
                    st.error(f"Error: {e}")
        
        elif tipo_calculo == "Evento complementario":
            st.markdown("**Probabilidad del evento complementario**")
            st.markdown("P(A') = 1 - P(A)")
            
            probabilidad_evento = st.slider(
                "Probabilidad del evento A",
                0.0,
                1.0,
                0.3,
                0.01,
                help="Probabilidad del evento original"
            )
            
            if st.button("Calcular Complemento", type="primary"):
                try:
                    resultado = probabilidad_complemento(probabilidad_evento)
                    
                    st.success(f"**P(A') = {resultado:.4f}**")
                    st.success(f"**Porcentaje = {resultado*100:.2f}%**")
                    st.info(
                        f"**Fórmula:** 1 - {probabilidad_evento:.4f} = "
                        f"{resultado:.4f}"
                    )
                    
                    # Verificación de la suma
                    suma = probabilidad_evento + resultado
                    st.info(
                        f"**Verificación:** P(A) + P(A') = "
                        f"{probabilidad_evento:.4f} + {resultado:.4f} = "
                        f"{suma:.4f}"
                    )
                    
                except ValueError as e:
                    st.error(f"Error: {e}")
        
        else:  # Unión de eventos independientes
            st.markdown("**Unión de eventos independientes**")
            st.markdown("P(A ∪ B) = P(A) + P(B) - P(A ∩ B)")
            
            p_a = st.slider(
                "Probabilidad del evento A",
                0.0,
                1.0,
                0.4,
                0.01
            )
            
            p_b = st.slider(
                "Probabilidad del evento B",
                0.0,
                1.0,
                0.3,
                0.01
            )
            
            if st.button("Calcular Unión", type="primary"):
                try:
                    resultado = probabilidad_union_eventos_independientes(
                        p_a,
                        p_b
                    )
                    
                    # Para eventos independientes
                    interseccion = p_a * p_b
                    
                    st.success(f"**P(A ∪ B) = {resultado:.4f}**")
                    st.success(f"**Porcentaje = {resultado*100:.2f}%**")
                    st.info(
                        f"**Fórmula:** {p_a:.4f} + {p_b:.4f} - "
                        f"{interseccion:.4f} = {resultado:.4f}"
                    )
                    st.info(
                        f"**P(A ∩ B) = {p_a:.4f} × {p_b:.4f} = "
                        f"{interseccion:.4f}**"
                    )
                    
                except ValueError as e:
                    st.error(f"Error: {e}")
    
    # Columna 2: Información adicional
    with col2:
        st.subheader("Información")
        
        # Axiomas de la probabilidad
        st.markdown("""
        **Axiomas de la Probabilidad:**
        1. P(A) ≥ 0 para todo evento A
        2. P(S) = 1 (espacio muestral completo)
        3. P(A ∪ B) = P(A) + P(B) si A y B son mutuamente excluyentes
        """)
        
        # Propiedades importantes
        st.markdown("""
        **Propiedades importantes:**
        - 0 ≤ P(A) ≤ 1
        - P(A') = 1 - P(A)
        - P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
        - Para eventos independientes: P(A ∩ B) = P(A) × P(B)
        """)
        
        # Aplicaciones
        st.markdown("""
        **Aplicaciones:**
        - Análisis de riesgo
        - Modelado estadístico
        - Análisis de confiabilidad
        - Simulaciones Monte Carlo
        """)
        
        # Ejemplos prácticos
        st.markdown("**Ejemplos prácticos:**")
        st.markdown("""
        - **Lanzar un dado:** P(6) = 1/6 ≈ 0.167
        - **Moneda justa:** P(cara) = 1/2 = 0.5
        - **Baraja:** P(as) = 4/52 ≈ 0.077
        - **Nacimiento:** P(niño) ≈ 0.512
        """)