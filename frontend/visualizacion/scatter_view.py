import streamlit as st
import pandas as pd
from backend.visualizacion import generar_grafico_dispersion

def render():
    st.title("📊 Gráfico de Dispersión (Scatter Plot)")

    st.markdown("""
    Sube un archivo CSV para generar un gráfico de dispersión. Esta herramienta te permite
    visualizar la relación entre dos variables numéricas.
    """)

    # 1. Carga del archivo
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

    if uploaded_file is not None:
        try:
            # 2. Lectura de datos con Pandas
            df = pd.read_csv(uploaded_file)
            st.success("¡Archivo cargado y leído correctamente!")
            
            st.subheader("Vista previa de los datos")
            st.dataframe(df.head())

            # 3. Selección de columnas para los ejes
            columnas = df.columns.tolist()
            col_x = st.selectbox("Selecciona la columna para el eje X", options=columnas, index=0)
            col_y = st.selectbox("Selecciona la columna para el eje Y", options=columnas, index=1 if len(columnas) > 1 else 0)

            # 4. Generación y muestra del gráfico
            if st.button("Generar Gráfico"):
                if col_x and col_y:
                    st.subheader(f"Visualización de {col_y} vs. {col_x}")
                    # Llamada a la función del backend
                    fig = generar_grafico_dispersion(df, col_x, col_y)
                    st.pyplot(fig)
                else:
                    st.warning("Por favor, selecciona columnas para ambos ejes.")

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")