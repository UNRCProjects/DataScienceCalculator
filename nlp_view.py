import streamlit as st

class NLPView:
    """Clase para renderizar la interfaz mínima del Módulo de NLP."""
    def render(self):
        st.title("🧠 Módulo de Análisis de Texto (NLP)")
        st.subheader("Clasificación de Requisitos de Vacantes/Perfiles")
        
        # Estructura del formulario
        input_text = st.text_area(
            "Pega la descripción de la vacante o perfil:",
            value="",
            height=200,
            key="nlp_input_text"
        )
        
        if st.button("🔍 Iniciar Análisis de Texto", type="primary"):
            if input_text:
                # ¡Aquí empezarás a codificar tu IA de NLP!
                st.success("Estructura funcional lista. ¡Puedes empezar a codificar tu IA aquí!")
            else:
                st.warning("Por favor, introduce texto para analizar.")

# Instancia para usar en el archivo principal
nlp_view = NLPView()