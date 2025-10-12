import streamlit as st
import pandas as pd
import numpy as np
from backend.probabilidad import (
    cargar_datos, 
    analisis_completo, 
    generar_reporte_estadistico,
    detectar_valores_vacios,
    rellenar_valores_vacios
)

def render():
    st.header("📊 Análisis Estadístico de Datos")
    st.markdown("""
    **Descripción:** Esta herramienta permite cargar un archivo de datos y realizar un análisis estadístico completo,
    incluyendo medidas de tendencia central, desviación estándar y manejo de valores vacíos.
    """)
    
    # Sidebar para configuración
    with st.sidebar:
        st.subheader("⚙️ Configuración")
        
        # Opciones para valores vacíos
        rellenar_vacios = st.checkbox("Rellenar valores vacíos", value=True)
        if rellenar_vacios:
            metodo_relleno = st.selectbox(
                "Método de relleno",
                options=['promedio', 'mediana', 'moda'],
                help="Promedio: Media aritmética\nMediana: Valor central\nModa: Valor más frecuente"
            )
        else:
            metodo_relleno = 'promedio'
    
    # Sección de carga de archivos
    st.subheader("📁 Carga de Datos")
    
    # Opción 1: Subir archivo
    archivo_subido = st.file_uploader(
        "Subir archivo CSV o Excel",
        type=['csv', 'xlsx', 'xls'],
        help="Formatos soportados: CSV, Excel (.xlsx, .xls)"
    )
    
    # Opción 2: Ruta de archivo local
    archivo_ruta = st.text_input(
        "O ingrese la ruta del archivo local",
        placeholder="ej: datos/mi_archivo.csv",
        help="Ruta relativa o absoluta al archivo"
    )
    
    # Determinar qué archivo usar
    archivo_path = None
    if archivo_subido is not None:
        archivo_path = archivo_subido
    elif archivo_ruta:
        archivo_path = archivo_ruta
    
    if archivo_path:
        try:
            # Mostrar información del archivo
            with st.expander("📋 Información del archivo", expanded=False):
                if hasattr(archivo_path, 'name'):
                    st.write(f"**Nombre:** {archivo_path.name}")
                    st.write(f"**Tipo:** {archivo_path.type}")
                else:
                    st.write(f"**Ruta:** {archivo_path}")
            
            # Cargar y mostrar vista previa de los datos
            try:
                df = cargar_datos(archivo_path)
                
                st.subheader("👁️ Vista previa de los datos")
                st.dataframe(df.head(10))
                
                # Información básica del dataset
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de filas", len(df))
                with col2:
                    st.metric("Total de columnas", len(df.columns))
                with col3:
                    columnas_numericas = len(df.select_dtypes(include=[np.number]).columns)
                    st.metric("Columnas numéricas", columnas_numericas)
                
                # Selección de columna específica
                if columnas_numericas > 0:
                    st.subheader("🎯 Análisis específico")
                    
                    columna_seleccionada = st.selectbox(
                        "Seleccionar columna para análisis detallado",
                        options=['Todas las columnas numéricas'] + list(df.select_dtypes(include=[np.number]).columns),
                        help="Seleccione una columna específica o analice todas las columnas numéricas"
                    )
                    
                    if columna_seleccionada == 'Todas las columnas numéricas':
                        columna_analisis = None
                    else:
                        columna_analisis = columna_seleccionada
                    
                    # Botón para realizar análisis
                    if st.button("🔍 Realizar Análisis Estadístico", type="primary"):
                        with st.spinner("Procesando datos..."):
                            # Realizar análisis completo
                            analisis = analisis_completo(
                                archivo_path, 
                                columna_analisis, 
                                rellenar_vacios, 
                                metodo_relleno
                            )
                            
                            # Mostrar resultados
                            mostrar_resultados(analisis, metodo_relleno)
                else:
                    st.warning("⚠️ No se encontraron columnas numéricas en el archivo.")
                    
            except Exception as e:
                st.error(f"Error al procesar el archivo: {str(e)}")
                
        except Exception as e:
            st.error(f"Error al cargar el archivo: {str(e)}")

def mostrar_resultados(analisis, metodo_relleno):
    """Muestra los resultados del análisis estadístico"""
    
    st.subheader("📈 Resultados del Análisis")
    
    # Información de valores vacíos
    info_vacios = analisis['info_valores_vacios']
    if any(info_vacios['valores_vacios'].values()):
        st.subheader("🔍 Valores Vacíos Detectados")
        
        vacios_df = pd.DataFrame({
            'Columna': list(info_vacios['valores_vacios'].keys()),
            'Valores vacíos': list(info_vacios['valores_vacios'].values()),
            'Porcentaje': [f"{info_vacios['porcentaje_vacios'][col]:.1f}%" 
                          for col in info_vacios['valores_vacios'].keys()]
        })
        
        st.dataframe(vacios_df, use_container_width=True)
        
        if any(v > 0 for v in info_vacios['valores_vacios'].values()):
            st.info(f"ℹ️ Los valores vacíos fueron rellenados usando el método: **{metodo_relleno}**")
    else:
        st.success("✅ No se encontraron valores vacíos en el dataset.")
    
    # Medidas de tendencia central
    st.subheader("📊 Medidas de Tendencia Central")
    
    for columna, medidas in analisis['medidas_tendencia_central'].items():
        with st.expander(f"📈 {columna}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Media", f"{medidas['media']:.4f}")
                st.metric("Mediana", f"{medidas['mediana']:.4f}")
            
            with col2:
                st.metric("Mínimo", f"{medidas['minimo']:.4f}")
                st.metric("Máximo", f"{medidas['maximo']:.4f}")
            
            with col3:
                st.metric("Q1 (25%)", f"{medidas['cuartil_25']:.4f}")
                st.metric("Q3 (75%)", f"{medidas['cuartil_75']:.4f}")
            
            with col4:
                st.metric("Rango", f"{medidas['rango']:.4f}")
                if medidas['moda']:
                    st.metric("Moda", f"{medidas['moda'][0]:.4f}")
                else:
                    st.metric("Moda", "Sin moda")
    
    # Medidas de dispersión
    st.subheader("📏 Medidas de Dispersión")
    
    for columna, medidas in analisis['medidas_dispersion'].items():
        with st.expander(f"📊 {columna}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Desv. Estándar", f"{medidas['desviacion_estandar']:.4f}")
            
            with col2:
                st.metric("Varianza", f"{medidas['varianza']:.4f}")
            
            with col3:
                st.metric("Coef. Variación", f"{medidas['coeficiente_variacion']:.2f}%")
            
            with col4:
                st.metric("Rango Intercuartílico", f"{medidas['rango_intercuartilico']:.4f}")
    
    # Resumen estadístico
    st.subheader("📋 Resumen Estadístico")
    st.dataframe(analisis['resumen_estadistico'], use_container_width=True)
    
    # Gráficos
    if len(analisis['columnas_numericas']) > 0:
        st.subheader("📈 Visualizaciones")
        
        columna_grafico = st.selectbox(
            "Seleccionar columna para gráficos",
            analisis['columnas_numericas']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Histograma")
            st.bar_chart(analisis['datos_originales'][columna_grafico])
        
        with col2:
            st.subheader("Datos vs Índice")
            st.line_chart(analisis['datos_originales'][columna_grafico])
    
    # Reporte completo
    st.subheader("📄 Reporte Completo")
    if st.button("📋 Generar Reporte"):
        reporte = generar_reporte_estadistico(analisis)
        st.text_area("Reporte Estadístico", reporte, height=400)
        
        # Opción para descargar el reporte
        st.download_button(
            label="💾 Descargar Reporte",
            data=reporte,
            file_name="reporte_estadistico.txt",
            mime="text/plain"
        )
