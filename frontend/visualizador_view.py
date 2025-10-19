# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from backend.visualizador import (
    cargar_datos,
    convertir_a_numerico,
    manejar_nulos,
    analisis_estadistico,
    generar_tabla_frecuencia,
    generar_diagrama_dispersion,
    generar_grafico_pastel,
    generar_histograma,
    generar_diagrama_caja,
    generar_mapa_calor,
    generar_regresion_lineal
)


def limpiar_datos_automaticamente(df):
    """
    Limpia automaticamente el DataFrame manejando solo valores nulos (NaN/null).
    NO convierte tipos de datos, solo limpia valores faltantes.

    Args:
        df (pandas.DataFrame): DataFrame a limpiar

    Returns:
        pandas.DataFrame: DataFrame limpio
    """
    df_limpio = df.copy()

    for columna in df_limpio.columns:
        # Solo procesar si hay valores nulos
        if df_limpio[columna].isna().sum() > 0:
            # Manejar nulos con estrategia de media para columnas numericas
            if pd.api.types.is_numeric_dtype(df_limpio[columna]):
                df_limpio = manejar_nulos(df_limpio, columna, estrategia='media')
            else:
                # Para columnas categoricas/texto, usar moda
                df_limpio = manejar_nulos(df_limpio, columna, estrategia='moda')

    return df_limpio


def render():
    st.header("📊 Visualizador de Datos")
    st.markdown("""
    **Descripcion:** Este modulo permite cargar archivos de datos (CSV o Excel),
    y generar visualizaciones interactivas para analisis de datos.
    """)

    # ============ SECCION 1: CARGA DE DATOS ============
    st.markdown("---")
    st.subheader("📁 Paso 1: Cargar Archivo de Datos")

    archivo = st.file_uploader(
        "Seleccione un archivo CSV o Excel",
        type=['csv', 'xls', 'xlsx'],
        help="Formatos soportados: .csv, .xls, .xlsx"
    )

    if archivo is not None:
        try:
            # Cargar datos
            df_original = cargar_datos(archivo)

            # Limpiar datos automaticamente
            df = limpiar_datos_automaticamente(df_original)

            # Guardar en session_state
            st.session_state['dataframe'] = df
            st.session_state['dataframe_original'] = df_original

            st.success(f"✅ Archivo cargado y limpiado exitosamente: **{archivo.name}**")

            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📋 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
            with col2:
                nulos_antes = df_original.isna().sum().sum()
                nulos_despues = df.isna().sum().sum()
                st.info(f"🧹 Valores nulos limpiados: {nulos_antes} → {nulos_despues}")

            # Mostrar vista previa
            with st.expander("👁️ Ver vista previa de los datos"):
                st.dataframe(df.head(10), use_container_width=True)

                # Mostrar informacion de columnas
                st.markdown("**Informacion de columnas:**")
                info_df = pd.DataFrame({
                    'Columna': df.columns,
                    'Tipo': df.dtypes.astype(str),
                    'Valores Unicos': [df[col].nunique() for col in df.columns],
                    'Nulos': [df[col].isna().sum() for col in df.columns]
                })
                st.dataframe(info_df, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")

    # ============ SECCION 2: VISUALIZACIONES ============
    if 'dataframe' in st.session_state:
        df = st.session_state['dataframe']

        st.markdown("---")
        st.subheader("📊 Paso 2: Generar Visualizaciones")

        # Dividir en dos columnas: selector de grafico y opciones
        col_selector, col_opciones = st.columns([1, 2])

        with col_selector:
            tipo_grafico = st.selectbox(
                "Tipo de grafico",
                options=[
                    "Grafico de Lineas",
                    "Grafico de Barras",
                    "Diagrama de Dispersion",
                    "Grafico de Pastel",
                    "Histograma",
                    "Diagrama de Caja",
                    "Mapa de Calor",
                    "Regresion Lineal"
                ]
            )

        with col_opciones:
            # Obtener columnas numericas y categoricas
            columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
            columnas_categoricas = df.select_dtypes(exclude=['number']).columns.tolist()
            todas_columnas = df.columns.tolist()

            # ---- GRAFICO DE LINEAS ----
            if tipo_grafico == "Grafico de Lineas":
                col1, col2 = st.columns(2)
                with col1:
                    eje_x = st.selectbox("Eje X", todas_columnas, key="lineas_x")
                with col2:
                    eje_y = st.selectbox("Eje Y (numerico)", columnas_numericas, key="lineas_y")

                if st.button("Generar grafico", key="lineas_btn"):
                    try:
                        import matplotlib.pyplot as plt
                        fig, ax = plt.subplots(figsize=(10, 6))

                        df_ordenado = df.sort_values(by=eje_x)
                        ax.plot(df_ordenado[eje_x], df_ordenado[eje_y],
                               marker='o', linewidth=2, markersize=6, color='steelblue')

                        ax.set_xlabel(eje_x, fontsize=12)
                        ax.set_ylabel(eje_y, fontsize=12)
                        ax.set_title(f'Grafico de Lineas: {eje_y} vs {eje_x}',
                                    fontsize=14, fontweight='bold')
                        ax.grid(True, alpha=0.3)
                        plt.xticks(rotation=45, ha='right')
                        plt.tight_layout()

                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            # ---- GRAFICO DE BARRAS ----
            elif tipo_grafico == "Grafico de Barras":
                col1, col2 = st.columns(2)
                with col1:
                    eje_x = st.selectbox("Eje X (categorias)", todas_columnas, key="barras_x")
                with col2:
                    eje_y = st.selectbox("Eje Y (valores)", columnas_numericas, key="barras_y")

                limite = st.slider("Numero maximo de categorias", 5, 50, 20, key="barras_limite")

                if st.button("Generar grafico", key="barras_btn"):
                    try:
                        import matplotlib.pyplot as plt
                        fig, ax = plt.subplots(figsize=(10, 6))

                        # Agrupar y ordenar datos
                        datos_agrupados = df.groupby(eje_x)[eje_y].sum().sort_values(ascending=False).head(limite)

                        ax.bar(range(len(datos_agrupados)), datos_agrupados.values,
                              color='steelblue', edgecolor='black')
                        ax.set_xticks(range(len(datos_agrupados)))
                        ax.set_xticklabels(datos_agrupados.index, rotation=45, ha='right')
                        ax.set_xlabel(eje_x, fontsize=12)
                        ax.set_ylabel(eje_y, fontsize=12)
                        ax.set_title(f'Grafico de Barras: {eje_y} por {eje_x}',
                                    fontsize=14, fontweight='bold')
                        ax.grid(axis='y', alpha=0.3)
                        plt.tight_layout()

                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            # ---- DIAGRAMA DE DISPERSION ----
            elif tipo_grafico == "Diagrama de Dispersion":
                col1, col2 = st.columns(2)
                with col1:
                    eje_x = st.selectbox("Eje X", columnas_numericas, key="scatter_x")
                with col2:
                    eje_y = st.selectbox("Eje Y", columnas_numericas, key="scatter_y")

                if st.button("Generar grafico", key="scatter_btn"):
                    try:
                        fig = generar_diagrama_dispersion(df, eje_x, eje_y)
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            # ---- GRAFICO DE PASTEL ----
            elif tipo_grafico == "Grafico de Pastel":
                col1, col2 = st.columns(2)
                with col1:
                    columna = st.selectbox("Columna", todas_columnas, key="pie_col")
                with col2:
                    limite = st.slider("Numero maximo de categorias", 3, 15, 10, key="pie_limite")

                if st.button("Generar grafico", key="pie_btn"):
                    try:
                        fig = generar_grafico_pastel(df, columna, limite)
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            # ---- HISTOGRAMA ----
            elif tipo_grafico == "Histograma":
                col1, col2 = st.columns(2)
                with col1:
                    columna = st.selectbox("Columna numerica", columnas_numericas, key="hist_col")
                with col2:
                    bins = st.slider("Numero de bins", 10, 100, 30, key="hist_bins")

                if st.button("Generar grafico", key="hist_btn"):
                    try:
                        fig = generar_histograma(df, columna, bins)
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            # ---- DIAGRAMA DE CAJA ----
            elif tipo_grafico == "Diagrama de Caja":
                columnas = st.multiselect(
                    "Seleccione una o mas columnas numericas",
                    columnas_numericas,
                    key="box_cols"
                )

                if st.button("Generar grafico", key="box_btn"):
                    if len(columnas) == 0:
                        st.warning("⚠️ Seleccione al menos una columna")
                    else:
                        try:
                            fig = generar_diagrama_caja(df, columnas)
                            st.pyplot(fig)
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

            # ---- MAPA DE CALOR ----
            elif tipo_grafico == "Mapa de Calor":
                columnas = st.multiselect(
                    "Seleccione columnas numericas",
                    columnas_numericas,
                    default=columnas_numericas[:min(5, len(columnas_numericas))],
                    key="heat_cols"
                )

                if st.button("Generar grafico", key="heat_btn"):
                    if len(columnas) < 2:
                        st.warning("⚠️ Seleccione al menos 2 columnas")
                    else:
                        try:
                            fig = generar_mapa_calor(df, columnas)
                            st.pyplot(fig)
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

            # ---- REGRESION LINEAL ----
            elif tipo_grafico == "Regresion Lineal":
                col1, col2 = st.columns(2)
                with col1:
                    eje_x = st.selectbox("Variable independiente (X)", columnas_numericas, key="reg_x")
                with col2:
                    eje_y = st.selectbox("Variable dependiente (Y)", columnas_numericas, key="reg_y")

                if st.button("Generar grafico", key="reg_btn"):
                    try:
                        fig, stats = generar_regresion_lineal(df, eje_x, eje_y)
                        st.pyplot(fig)

                        # Mostrar estadisticas de la regresion
                        st.markdown("**📊 Estadisticas de la Regresion:**")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("R2 (Coef. Determinacion)", f"{stats['r_cuadrado']:.4f}")
                        with col2:
                            st.metric("Correlacion", f"{stats['correlacion']:.4f}")
                        with col3:
                            st.metric("Pendiente", f"{stats['pendiente']:.4f}")

                        st.info(f"**Ecuacion:** {stats['ecuacion']}")

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        # ============ ANALISIS ESTADISTICO OPCIONAL ============
        st.markdown("---")
        with st.expander("📈 Analisis Estadistico (Opcional)"):
            st.markdown("Seleccione una columna para ver sus estadisticas detalladas:")

            columna_analisis = st.selectbox(
                "Columna",
                options=df.columns.tolist(),
                key="analisis_select"
            )

            if st.button("📊 Calcular estadisticas", key="stats_btn"):
                try:
                    stats = analisis_estadistico(df, columna_analisis)

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Total de datos", stats['total_datos'])
                        st.metric("Valores nulos", stats['valores_nulos'])

                    with col2:
                        st.metric("Valores unicos", stats['valores_unicos'])
                        if 'media' in stats:
                            st.metric("Media", f"{stats['media']:.2f}")

                    with col3:
                        if 'mediana' in stats:
                            st.metric("Mediana", f"{stats['mediana']:.2f}")
                        if 'desviacion_estandar' in stats:
                            st.metric("Desv. Estandar", f"{stats['desviacion_estandar']:.2f}")

                    # Mostrar estadisticas detalladas
                    st.markdown("---")
                    st.markdown("**Estadisticas Detalladas:**")

                    col1, col2 = st.columns(2)

                    with col1:
                        for clave, valor in stats.items():
                            if clave not in ['frecuencias', 'total_datos', 'valores_nulos',
                                           'valores_unicos', 'media', 'mediana', 'desviacion_estandar']:
                                if isinstance(valor, (int, float)):
                                    st.write(f"**{clave.replace('_', ' ').title()}:** {valor:.4f}")
                                else:
                                    st.write(f"**{clave.replace('_', ' ').title()}:** {valor}")

                    with col2:
                        # Mostrar tabla de frecuencias
                        if 'frecuencias' in stats and len(stats['frecuencias']) > 0:
                            st.markdown("**Tabla de Frecuencias (Top 10):**")
                            freq_df = pd.DataFrame(
                                list(stats['frecuencias'].items()),
                                columns=['Valor', 'Frecuencia']
                            ).head(10)
                            st.dataframe(freq_df, use_container_width=True)

                except Exception as e:
                    st.error(f"❌ Error en analisis: {str(e)}")

    else:
        st.info("👆 Por favor, cargue un archivo de datos en el Paso 1 para comenzar.")
