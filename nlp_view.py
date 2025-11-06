import streamlit as st
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Descargar recursos de NLTK si no están instalados
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Lista de stopwords en español para limpieza
spanish_stopwords = set(stopwords.words('spanish'))

class NLPView:
    """Clase para renderizar la interfaz y lógica del Módulo de Análisis de Texto Descriptivo."""
    
    def preprocess_text(self, text):
        """Limpia y tokeniza el texto: minúsculas, eliminación de stopwords y puntuación."""
        text = text.lower()
        tokens = word_tokenize(text, language='spanish')
        processed_tokens = [word for word in tokens if word.isalpha() and word not in spanish_stopwords]
        return processed_tokens

    def analyze_descriptive(self, input_text):
        """Realiza el análisis de frecuencias y métricas descriptivas."""
        processed_tokens = self.preprocess_text(input_text)
        total_words = len(processed_tokens)
        unique_words = len(set(processed_tokens))
        word_counts = Counter(processed_tokens)
        top_10 = word_counts.most_common(10)
        return total_words, unique_words, top_10

    def render(self):
        st.title("📊 Análisis Descriptivo de Texto General")
        st.subheader("Herramienta para Científicos de Datos: Frecuencia y Limpieza")
        
        input_text = st.text_area(
            "Pega el texto a analizar (ej. descripciones de perfil, artículos, reportes):",
            value="",
            height=300,
            key="nlp_input_text"
        )
        
        if st.button("🔍 Analizar Texto", type="primary"):
            if not input_text:
                st.warning("Por favor, introduce texto para analizar.")
                return

            with st.spinner('Realizando limpieza y conteo de frecuencias...'):
                total_words, unique_words, top_10 = self.analyze_descriptive(input_text)
                
                if total_words == 0:
                    st.info("No se detectaron palabras después del preprocesamiento.")
                    return

                st.success("Análisis Descriptivo Completo.")
                st.write("---")

                col1, col2, col3 = st.columns(3)
                col1.metric("Palabras (Tokens Limpios)", total_words)
                col2.metric("Palabras Únicas", unique_words)
                col3.metric("Diversidad Léxica", f"{unique_words / total_words:.2f}")

                st.markdown("#### 🔝 Top 10 de Palabras más Frecuentes (Sin Stopwords)")
                
                df_frecuencias = pd.DataFrame(top_10, columns=['Palabra', 'Frecuencia'])
                st.bar_chart(df_frecuencias.set_index('Palabra')['Frecuencia'])
                st.dataframe(df_frecuencias, use_container_width=True)

nlp_view = NLPView()
