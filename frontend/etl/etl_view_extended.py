import streamlit as st
import pandas as pd
import tempfile
import os
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from backend.etl.etl_utils import ETLProcessor

def render():
    st.title("Módulo ETL: Escaneo, Limpieza y Transformación de CSV")

    # 1. SUBIR ARCHIVO CSV
    uploaded_file = st.file_uploader("Sube un archivo CSV para procesar", type=["csv"])
    if uploaded_file is None:
        st.info("Por favor, sube un archivo CSV para comenzar.")
        return

    # Guardar archivo temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    etl = ETLProcessor(tmp_path)
    df = etl.load_csv()

    # 2. EXPLORAR
    st.header("🔍 Exploración del Dataset")
    st.subheader("Vista previa de los datos:")
    st.dataframe(df.head())

    st.subheader("Resumen general:")
    st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    st.write("Columnas:", df.columns.tolist())

    st.subheader("Valores nulos por columna:")
    st.bar_chart(df.isnull().sum())

    st.subheader("Tipos de datos:")
    st.write(df.dtypes.astype(str))

    st.subheader("Duplicados detectados:")
    n_dup = df.duplicated().sum()
    st.write(f"Filas duplicadas: {n_dup}")

    # 3. LIMPIAR
    st.header("🧹 Limpieza de Datos")
    cols_to_drop = st.multiselect("Selecciona columnas a eliminar", df.columns)
    impute_method = st.selectbox("Método para imputar valores nulos en columnas numéricas", ["media", "mediana", "cero"])
    if st.button("Aplicar limpieza"):
        df_clean = df.copy()
        if cols_to_drop:
            df_clean = df_clean.drop(columns=cols_to_drop)
        # Imputación de nulos
        num_cols = df_clean.select_dtypes(include='number').columns
        for col in num_cols:
            if impute_method == "media":
                df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
            elif impute_method == "mediana":
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            elif impute_method == "cero":
                df_clean[col] = df_clean[col].fillna(0)
        # Eliminar duplicados
        df_clean = df_clean.drop_duplicates()
        st.success("Limpieza aplicada.")
        st.dataframe(df_clean.head())
    else:
        df_clean = df

    # 4. TRANSFORMAR
    st.header("🔄 Transformaciones")
    with st.expander("Renombrar columnas"):
        rename_dict = {}
        for col in df_clean.columns:
            new_name = st.text_input(f"Nuevo nombre para '{col}'", value=col, key=f"rename_{col}")
            rename_dict[col] = new_name
        if st.button("Renombrar columnas"):
            df_clean = df_clean.rename(columns=rename_dict)
            st.success("Columnas renombradas.")
            st.dataframe(df_clean.head())

    with st.expander("Normalizar columnas numéricas"):
        cols_norm = st.multiselect("Selecciona columnas a normalizar (min-max)", df_clean.select_dtypes(include='number').columns, key="norm_cols")
        if st.button("Normalizar"):
            for col in cols_norm:
                min_val = df_clean[col].min()
                max_val = df_clean[col].max()
                if max_val != min_val:
                    df_clean[col] = (df_clean[col] - min_val) / (max_val - min_val)
            st.success("Columnas normalizadas.")
            st.dataframe(df_clean.head())

    with st.expander("Codificar variables categóricas"):
        cat_cols = st.multiselect("Selecciona columnas categóricas para codificar (one-hot)", df_clean.select_dtypes(include='object').columns, key="cat_cols")
        if st.button("Codificar"):
            df_clean = pd.get_dummies(df_clean, columns=cat_cols)
            st.success("Columnas codificadas.")
            st.dataframe(df_clean.head())

    # 5. VISUALIZAR
    st.header("📊 Visualización")
    with st.expander("Histogramas de columnas numéricas"):
        num_col = st.selectbox("Selecciona columna numérica", df_clean.select_dtypes(include='number').columns, key="hist_col")
        if st.button("Mostrar histograma"):
            fig, ax = plt.subplots()
            sns.histplot(df_clean[num_col], kde=True, ax=ax)
            st.pyplot(fig)

    with st.expander("Matriz de correlación"):
        if st.button("Mostrar correlación"):
            corr = df_clean.corr(numeric_only=True)
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    # 6. DESCARGAR
    st.header("⬇️ Descargar resultados")
    csv = df_clean.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="datos_limpios.csv">Descargar CSV limpio</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Eliminar archivo temporal
    os.remove(tmp_path)