import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from backend.probabilidad import (
    comparar_distribuciones, 
    generar_grafico_distribucion,
    calcular_probabilidad_acumulada,
    calcular_percentil,
    calcular_intervalo_confianza
)

def render():
    st.header("📊 Análisis de Distribuciones de Probabilidad")
    
    # Verificar si hay datos cargados
    if 'df_probabilidad' not in st.session_state:
        st.warning("⚠️ No hay datos cargados. Ve a 'Carga de Datos' primero.")
        if st.button("📁 Ir a Carga de Datos"):
            st.session_state['categoria'] = "Probabilidad"
            st.session_state['subopcion'] = "Carga de Datos"
            st.rerun()
        return
    
    df = st.session_state['df_probabilidad']
    columna = st.session_state['columna_probabilidad']
    stats = st.session_state['stats_probabilidad']
    
    st.subheader(f"📈 Análisis de la columna: **{columna}**")
    
    # Mostrar resumen de datos
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de datos", len(df[columna].dropna()))
    with col2:
        st.metric("Datos faltantes", df[columna].isna().sum())
    with col3:
        st.metric("Media", f"{stats['media']:.4f}")
    
    # Análisis de distribuciones
    st.subheader("🔍 Ajuste de Distribuciones")
    
    if st.button("🚀 Analizar Distribuciones", type="primary"):
        with st.spinner("Analizando distribuciones..."):
            try:
                datos = df[columna]
                distribuciones = comparar_distribuciones(datos)
                
                if not distribuciones:
                    st.error("No se pudieron ajustar distribuciones a los datos.")
                    return
                
                # Mostrar resultados
                st.subheader("📊 Resultados del Ajuste")
                
                # Crear tabla de comparación
                resultados_data = []
                for dist in distribuciones:
                    resultados_data.append({
                        'Distribución': dist['tipo'],
                        'KS Statistic': f"{dist['test']['ks_statistic']:.6f}",
                        'P-value': f"{dist['test']['p_value']:.6f}",
                        'Ajuste': "✅ Bueno" if dist['test']['p_value'] > 0.05 else "❌ Rechazado"
                    })
                
                resultados_df = pd.DataFrame(resultados_data)
                st.dataframe(resultados_df, use_container_width=True)
                
                # Guardar distribuciones en session state
                st.session_state['distribuciones_probabilidad'] = distribuciones
                
                # Mostrar la mejor distribución
                mejor_dist = distribuciones[0]
                st.success(f"🏆 **Mejor ajuste:** {mejor_dist['tipo']} (p-value: {mejor_dist['test']['p_value']:.6f})")
                
                # Mostrar parámetros de la mejor distribución
                st.subheader("⚙️ Parámetros de la Mejor Distribución")
                parametros = mejor_dist['parametros']
                for param, valor in parametros.items():
                    st.write(f"**{param}:** {valor:.6f}")
                
                # Generar y mostrar gráfico
                st.subheader("📈 Gráfico de Ajuste")
                try:
                    imagen_base64 = generar_grafico_distribucion(datos, mejor_dist)
                    st.image(f"data:image/png;base64,{imagen_base64}", use_container_width=True)
                except Exception as e:
                    st.error(f"Error al generar gráfico: {str(e)}")
                
            except Exception as e:
                st.error(f"Error en el análisis: {str(e)}")
    
    # Cálculos de probabilidad
    if 'distribuciones_probabilidad' in st.session_state:
        st.subheader("🧮 Cálculos de Probabilidad")
        
        distribuciones = st.session_state['distribuciones_probabilidad']
        mejor_dist = distribuciones[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Probabilidad Acumulada")
            st.markdown("Calcula P(X ≤ valor)")
            
            valor_prob = st.number_input(
                "Valor:",
                value=float(stats['media']),
                step=0.1,
                format="%.4f"
            )
            
            if st.button("Calcular P(X ≤ valor)"):
                try:
                    prob_acum = calcular_probabilidad_acumulada(mejor_dist, valor_prob)
                    st.success(f"P(X ≤ {valor_prob}) = {prob_acum:.6f}")
                    st.write(f"**Interpretación:** {prob_acum*100:.2f}% de los datos son menores o iguales a {valor_prob}")
                except Exception as e:
                    st.error(f"Error en el cálculo: {str(e)}")
        
        with col2:
            st.subheader("📈 Percentiles")
            st.markdown("Calcula el valor para una probabilidad dada")
            
            probabilidad = st.slider(
                "Probabilidad:",
                min_value=0.01,
                max_value=0.99,
                value=0.5,
                step=0.01,
                format="%.2f"
            )
            
            if st.button("Calcular Percentil"):
                try:
                    percentil = calcular_percentil(mejor_dist, probabilidad)
                    st.success(f"Percentil {probabilidad*100:.1f}% = {percentil:.6f}")
                    st.write(f"**Interpretación:** {probabilidad*100:.1f}% de los datos son menores o iguales a {percentil:.4f}")
                except Exception as e:
                    st.error(f"Error en el cálculo: {str(e)}")
        
        # Intervalo de confianza
        st.subheader("🎯 Intervalo de Confianza")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nivel_confianza = st.selectbox(
                "Nivel de confianza:",
                [0.90, 0.95, 0.99],
                index=1,
                format_func=lambda x: f"{x*100:.0f}%"
            )
        
        with col2:
            if st.button("Calcular Intervalo"):
                try:
                    lim_inf, lim_sup = calcular_intervalo_confianza(mejor_dist, nivel_confianza)
                    st.success(f"Intervalo de confianza al {nivel_confianza*100:.0f}%:")
                    st.write(f"**[{lim_inf:.4f}, {lim_sup:.4f}]**")
                    st.write(f"**Interpretación:** Con {nivel_confianza*100:.0f}% de confianza, los valores están entre {lim_inf:.4f} y {lim_sup:.4f}")
                except Exception as e:
                    st.error(f"Error en el cálculo: {str(e)}")
        
        # Comparación de distribuciones
        st.subheader("🔄 Comparar Distribuciones")
        
        if len(distribuciones) > 1:
            dist_seleccionada = st.selectbox(
                "Selecciona una distribución para comparar:",
                [dist['tipo'] for dist in distribuciones[1:]]
            )
            
            if st.button("Mostrar Comparación"):
                dist_comp = next(dist for dist in distribuciones if dist['tipo'] == dist_seleccionada)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**{mejor_dist['tipo']} (Mejor)**")
                    st.write(f"P-value: {mejor_dist['test']['p_value']:.6f}")
                    st.write("Parámetros:")
                    for param, valor in mejor_dist['parametros'].items():
                        st.write(f"- {param}: {valor:.6f}")
                
                with col2:
                    st.write(f"**{dist_comp['tipo']} (Comparación)**")
                    st.write(f"P-value: {dist_comp['test']['p_value']:.6f}")
                    st.write("Parámetros:")
                    for param, valor in dist_comp['parametros'].items():
                        st.write(f"- {param}: {valor:.6f}")
                
                # Generar gráfico comparativo
                try:
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                    
                    datos = df[columna].dropna()
                    
                    # Gráfico 1: Mejor distribución
                    ax1.hist(datos, bins=30, density=True, alpha=0.7, color='skyblue')
                    x = np.linspace(datos.min(), datos.max(), 1000)
                    y1 = mejor_dist['pdf'](x)
                    ax1.plot(x, y1, 'r-', linewidth=2, label=mejor_dist['tipo'])
                    ax1.set_title(f'Distribución {mejor_dist["tipo"]}')
                    ax1.legend()
                    ax1.grid(True, alpha=0.3)
                    
                    # Gráfico 2: Distribución de comparación
                    ax2.hist(datos, bins=30, density=True, alpha=0.7, color='lightgreen')
                    y2 = dist_comp['pdf'](x)
                    ax2.plot(x, y2, 'b-', linewidth=2, label=dist_comp['tipo'])
                    ax2.set_title(f'Distribución {dist_comp["tipo"]}')
                    ax2.legend()
                    ax2.grid(True, alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                    
                except Exception as e:
                    st.error(f"Error al generar gráfico comparativo: {str(e)}")
    
    # Botón para volver a carga de datos
    if st.button("🔄 Cargar Nuevos Datos"):
        # Limpiar session state
        keys_to_remove = ['df_probabilidad', 'columna_probabilidad', 'stats_probabilidad', 'distribuciones_probabilidad']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state['categoria'] = "Probabilidad"
        st.session_state['subopcion'] = "Carga de Datos"
        st.rerun()
