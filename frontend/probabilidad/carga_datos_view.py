import streamlit as st
import pandas as pd
from backend.probabilidad import cargar_datos, estadisticas_descriptivas

def render():
    st.header("📊 Carga de Datos")
    st.markdown("""
    **Descripción:** Carga un archivo CSV o Excel para analizar distribuciones de probabilidad.
    """)
    
    # Carga de archivo
    archivo = st.file_uploader(
        "Selecciona un archivo CSV o Excel",
        type=['csv', 'xlsx', 'xls'],
        help="Formatos soportados: CSV, Excel (.xlsx, .xls)"
    )
    
    if archivo is not None:
        try:
            # Cargar datos
            df = cargar_datos(archivo)
            
            # Mostrar información del archivo
            st.success(f"✅ Archivo cargado exitosamente: {archivo.name}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Información del Dataset")
                st.write(f"**Filas:** {df.shape[0]}")
                st.write(f"**Columnas:** {df.shape[1]}")
                st.write(f"**Memoria:** {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            with col2:
                st.subheader("📊 Primeras 5 filas")
                st.dataframe(df.head(), use_container_width=True)
            
            # Selección de columna para análisis
            st.subheader("🎯 Selección de Columna")
            
            # Filtrar solo columnas numéricas
            columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(columnas_numericas) == 0:
                st.warning("⚠️ No se encontraron columnas numéricas en el dataset.")
                return
            
            columna_seleccionada = st.selectbox(
                "Selecciona una columna numérica para el análisis:",
                columnas_numericas,
                help="Solo se muestran columnas con datos numéricos"
            )
            
            if columna_seleccionada:
                # Mostrar estadísticas descriptivas
                st.subheader("📈 Estadísticas Descriptivas")
                
                try:
                    stats = estadisticas_descriptivas(df, columna_seleccionada)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Media", f"{stats['media']:.4f}")
                        st.metric("Mediana", f"{stats['mediana']:.4f}")
                        st.metric("Desv. Estándar", f"{stats['desviacion_estandar']:.4f}")
                    
                    with col2:
                        st.metric("Mínimo", f"{stats['minimo']:.4f}")
                        st.metric("Máximo", f"{stats['maximo']:.4f}")
                        st.metric("Varianza", f"{stats['varianza']:.4f}")
                    
                    with col3:
                        st.metric("Q1 (25%)", f"{stats['cuartil_25']:.4f}")
                        st.metric("Q3 (75%)", f"{stats['cuartil_75']:.4f}")
                        st.metric("Asimetría", f"{stats['asimetria']:.4f}")
                    
                    # Mostrar curtosis
                    st.metric("Curtosis", f"{stats['curtosis']:.4f}")
                    
                    # Guardar datos en session state para usar en otras vistas
                    st.session_state['df_probabilidad'] = df
                    st.session_state['columna_probabilidad'] = columna_seleccionada
                    st.session_state['stats_probabilidad'] = stats
                    
                    st.success("✅ Datos preparados para análisis de distribuciones")
                    
                    # Botón para ir a análisis de distribuciones
                    if st.button("🔍 Analizar Distribuciones", type="primary"):
                        st.session_state['categoria'] = "Probabilidad"
                        st.session_state['subopcion'] = "Distribuciones"
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error al calcular estadísticas: {str(e)}")
        
        except Exception as e:
            st.error(f"Error al cargar el archivo: {str(e)}")
    
    else:
        st.info("👆 Por favor, carga un archivo para comenzar el análisis.")
        
        # Mostrar ejemplo de formato
        st.subheader("📝 Formato de Archivo Esperado")
        st.markdown("""
        El archivo debe contener al menos una columna con datos numéricos. Ejemplo:
        
        | ID | Valor | Categoria |
        |----|-------|-----------|
        | 1  | 12.5  | A         |
        | 2  | 15.3  | B         |
        | 3  | 8.7   | A         |
        | 4  | 22.1  | C         |
        """)
