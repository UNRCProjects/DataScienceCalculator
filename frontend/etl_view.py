import streamlit as st
import tempfile
import os
from backend.etl.etl_utils import ETLProcessor

def render():
    st.title("Módulo ETL: Escaneo y Limpieza de CSV")
    uploaded_file = st.file_uploader("Sube un archivo CSV para procesar", type=["csv"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        etl = ETLProcessor(tmp_path)
        df = etl.load_csv()
        st.subheader("Vista previa de los datos cargados:")
        st.dataframe(df.head())
        if st.button("Limpiar datos (ETL)"):
            df_clean = etl.clean_data()
            st.success("Datos limpiados correctamente.")
            st.subheader("Datos después de limpieza:")
            st.dataframe(df_clean.head())
            st.subheader("Resumen estadístico:")
            st.dataframe(etl.get_summary())
        # Eliminar archivo temporal
        os.remove(tmp_path)
