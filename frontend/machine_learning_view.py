import streamlit as st
import pandas as pd
from backend.machine_learning import entrenar_modelo_clasificacion, entrenar_modelo_regresion

def render():
    st.header("Módulo: Machine Learning")
    st.markdown("""
    Sube un archivo CSV con tus datos, selecciona las columnas de características (features) y la columna objetivo (target),
    elige si quieres entrenar un modelo de clasificación o regresión y presiona Entrenar.
    """)

    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"No se pudo leer el archivo CSV: {e}")
            return

        st.success("CSV cargado correctamente")
        st.markdown("**Vista previa de los datos (primeras filas):**")
        st.dataframe(df.head())

        cols = list(df.columns)
        st.markdown("**Selecciona las columnas de entrada (features)**")
        features = st.multiselect("Features", cols, default=cols[:-1])
        st.markdown("**Selecciona la columna objetivo (target)**")
        target = st.selectbox("Target", cols, index=len(cols)-1 if len(cols) > 0 else 0)

        # detectar si el target parece continuo
        target_dtype = df[target].dtype
        unique_vals = df[target].nunique(dropna=True)
        is_continuous = pd.api.types.is_float_dtype(df[target]) or unique_vals > 20

        task = st.selectbox("Tarea", ["Clasificación", "Regresión"], index=1 if is_continuous else 0)

        if task == "Clasificación":
            modelo = st.selectbox("Modelo", ["RandomForest", "LogisticRegression", "SVM", "DecisionTree", "NaiveBayes"])
        else:
            modelo = st.selectbox("Modelo (Regresión)", ["RandomForest", "LinearRegression", "SVR", "DecisionTree"])

        if st.button("Entrenar modelo"):
            # Validaciones
            if not features:
                st.warning("Selecciona al menos una columna de features.")
            elif target in features:
                st.warning("La columna target no puede estar entre las features.")
            else:
                try:
                    if task == "Clasificación":
                        acc, reporte = entrenar_modelo_clasificacion(df, features, target, modelo=modelo)
                        st.success(f"Accuracy (conjunto de test): {acc:.4f}")
                        st.markdown("**Reporte de clasificación:**")
                        st.text(reporte)
                    else:
                        mse, r2, y_test, y_pred = entrenar_modelo_regresion(df, features, target, modelo=modelo)
                        st.success(f"MSE: {mse:.4f} — R2: {r2:.4f}")
                        st.markdown("**Ejemplo: valores reales vs predichos (primeras 10 filas)**")
                        comp = pd.DataFrame({'y_true': list(y_test)[:10], 'y_pred': list(y_pred)[:10]})
                        st.dataframe(comp)
                except Exception as e:
                    st.error(f"Error al entrenar el modelo: {e}")

    else:
        st.info("Sube un archivo CSV para comenzar. Puedes usar datasets pequeños tipo Iris o un CSV propio.")
