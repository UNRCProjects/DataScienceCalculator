import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from backend.combinatoria_y_probabilidad import (
    probabilidad_binomial,
    probabilidad_binomial_acumulada,
    combinacion
)


def render():
    """Renderiza la vista de la calculadora de distribución binomial."""
    
    # Encabezado principal
    st.header("📈 Distribución Binomial")
    
    # Definición y parámetros
    st.markdown("""
    **Definición:** La distribución binomial modela el número de éxitos en una 
    secuencia de n ensayos independientes de Bernoulli, cada uno con probabilidad 
    de éxito p.
    
    **Parámetros:**
    - n: número de ensayos
    - p: probabilidad de éxito en cada ensayo
    - k: número de éxitos observados
    """)
    
    # Layout en dos columnas
    col1, col2 = st.columns([1, 1])
    
    # Columna 1: Calculadora
    with col1:
        st.subheader("Calculadora")
        
        # Parámetros de la distribución
        n = st.number_input(
            "n (número de ensayos)",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            help="Número total de ensayos independientes"
        )
        
        p = st.slider(
            "p (probabilidad de éxito)",
            0.0,
            1.0,
            0.5,
            0.01,
            help="Probabilidad de éxito en cada ensayo"
        )
        
        tipo_calculo = st.selectbox(
            "Tipo de cálculo:",
            [
                "Probabilidad exacta",
                "Probabilidad acumulada (≤)",
                "Probabilidad acumulada (≥)"
            ],
            help="Diferentes tipos de probabilidades binomiales"
        )
        
        # Input de k según el tipo de cálculo
        if tipo_calculo == "Probabilidad exacta":
            k = st.number_input(
                "k (éxitos exactos)",
                min_value=0,
                max_value=n,
                value=5,
                step=1,
                help="Número exacto de éxitos"
            )
        else:
            k = st.number_input(
                "k (éxitos)",
                min_value=0,
                max_value=n,
                value=5,
                step=1,
                help="Número de éxitos para cálculo acumulado"
            )
        
        if st.button("Calcular", type="primary"):
            try:
                if tipo_calculo == "Probabilidad exacta":
                    resultado = probabilidad_binomial(n, k, p)
                    st.success(f"**P(X = {k}) = {resultado:.6f}**")
                    st.success(f"**Porcentaje = {resultado*100:.4f}%**")
                    
                    # Mostrar fórmula
                    st.info(
                        f"**Fórmula:** C({n},{k}) × {p}^{k} × {1-p}^{n-k}"
                    )
                    
                    combinaciones = combinacion(n, k)
                    prob_exito = p ** k
                    prob_fracaso = (1 - p) ** (n - k)
                    
                    st.info(
                        f"**Cálculo:** {combinaciones:,} × {prob_exito:.6f} × "
                        f"{prob_fracaso:.6f} = {resultado:.6f}"
                    )
                    
                else:
                    # Probabilidad acumulada
                    tipo_acum = (
                        "menor_igual"
                        if tipo_calculo == "Probabilidad acumulada (≤)"
                        else "mayor_igual"
                    )
                    resultado = probabilidad_binomial_acumulada(
                        n, k, p, tipo_acum
                    )
                    
                    simbolo = "≤" if tipo_acum == "menor_igual" else "≥"
                    st.success(f"**P(X {simbolo} {k}) = {resultado:.6f}**")
                    st.success(f"**Porcentaje = {resultado*100:.4f}%**")
                
                # Interpretación práctica
                st.markdown("**Interpretación práctica:**")
                
                if tipo_calculo == "Probabilidad exacta":
                    st.info(
                        f"En {n} ensayos con probabilidad de éxito {p}, "
                        f"la probabilidad de obtener exactamente {k} éxitos "
                        f"es {resultado*100:.2f}%"
                    )
                elif tipo_calculo == "Probabilidad acumulada (≤)":
                    st.info(
                        f"En {n} ensayos con probabilidad de éxito {p}, "
                        f"la probabilidad de obtener {k} éxitos o menos "
                        f"es {resultado*100:.2f}%"
                    )
                else:
                    st.info(
                        f"En {n} ensayos con probabilidad de éxito {p}, "
                        f"la probabilidad de obtener {k} éxitos o más "
                        f"es {resultado*100:.2f}%"
                    )
                    
            except ValueError as e:
                st.error(f"Error: {e}")
    
    # Columna 2: Información adicional
    with col2:
        st.subheader("Información")
        
        st.markdown("""
        **Características de la distribución binomial:**
        - **Media:** μ = n × p
        - **Varianza:** σ² = n × p × (1-p)
        - **Desviación estándar:** σ = √(n × p × (1-p))
        """)
        
        # Calcular estadísticas si hay parámetros válidos
        try:
            if n > 0 and 0 <= p <= 1:
                media = n * p
                varianza = n * p * (1 - p)
                desviacion = np.sqrt(varianza)
                
                st.markdown(f"**Estadísticas para n={n}, p={p:.2f}:**")
                st.text(f"• Media: {media:.2f}")
                st.text(f"• Varianza: {varianza:.2f}")
                st.text(f"• Desviación estándar: {desviacion:.2f}")
        except Exception:
            pass
        
        # Aplicaciones
        st.markdown("""
        **Aplicaciones:**
        - Control de calidad
        - Análisis de encuestas
        - Pruebas A/B
        - Modelado de eventos binarios
        - Análisis de confiabilidad
        """)
        
        # Ejemplos prácticos
        st.markdown("""
        **Ejemplos prácticos:**
        - Número de defectos en una muestra
        - Número de respuestas correctas en un examen
        - Número de clientes que compran un producto
        - Número de días lluviosos en un mes
        """)
    
    # Gráfico de la distribución
    if n <= 50 and n > 0 and 0 < p < 1:
        st.subheader("📊 Gráfico de la Distribución")
        
        try:
            # Generar valores para el gráfico
            x = np.arange(0, n + 1)
            y = [probabilidad_binomial(n, k_val, p) for k_val in x]
            
            # Crear el gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(
                x,
                y,
                alpha=0.7,
                color='skyblue',
                edgecolor='navy'
            )
            ax.set_xlabel('Número de éxitos (k)')
            ax.set_ylabel('Probabilidad')
            ax.set_title(f'Distribución Binomial (n={n}, p={p:.2f})')
            ax.grid(True, alpha=0.3)
            
            # Marcar la media
            media = n * p
            ax.axvline(
                media,
                color='red',
                linestyle='--',
                linewidth=2,
                label=f'Media = {media:.2f}'
            )
            ax.legend()
            
            st.pyplot(fig)
            
        except Exception as e:
            st.warning(f"No se pudo generar el gráfico: {e}")