import streamlit as st
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

import nltk

# Descargar recursos si no existen
nltk.download('punkt')
nltk.download('punkt_tab') 
nltk.download('stopwords')


import nltk

# Descargar recursos si no existen
nltk.download('punkt')
nltk.download('stopwords')



# Nota: Asegúrate que NLTK y los recursos 'stopwords' y 'punkt' estén instalados para todo el equipo.
# (Pip install nltk, y luego nltk.download('stopwords') y nltk.download('punkt') si es necesario).

# Lista de stopwords en español para limpieza
spanish_stopwords = set(stopwords.words('spanish'))

class NLPView:
    """Clase para renderizar la interfaz y lógica del Módulo de Análisis de Texto Descriptivo."""
    
    def preprocess_text(self, text):
        """Limpia y tokeniza el texto: minúsculas, eliminación de stopwords y puntuación."""
        text = text.lower()
        # Tokenización
        tokens = word_tokenize(text, language='spanish')
        
        # Eliminación de Stopwords, puntuación y números
        processed_tokens = [
            word for word in tokens 
            if word.isalpha() and word not in spanish_stopwords
        ]
        return processed_tokens

    def analyze_descriptive(self, input_text):
        """Realiza el análisis de frecuencias y métricas descriptivas."""
        
        # 1. Preprocesamiento
        processed_tokens = self.preprocess_text(input_text)
        
        # 2. Métricas Descriptivas
        total_words = len(processed_tokens)
        unique_words = len(set(processed_tokens))
        
        # 3. Conteo de Frecuencias
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
                
                st.success("Análisis Descriptivo Completo.")
                st.write("---")

                # Visualización 1: Métricas Clave
                col1, col2, col3 = st.columns(3)
                
                col1.metric("Palabras (Tokens Limpios)", total_words)
                col2.metric("Palabras Únicas", unique_words)
                col3.metric("Diversidad Léxica", f"{unique_words / total_words:.2f}" if total_words > 0 else "0.00")
                
                st.write("---")

                # Visualización 2: Top 10 de Palabras más Frecuentes
                st.markdown("#### 🔝 Top 10 de Palabras más Frecuentes")
                
                df_frecuencias = pd.DataFrame(top_10, columns=['Palabra', 'Frecuencia'])
                
                if not df_frecuencias.empty:
                    # Muestra un gráfico de barras
                    st.bar_chart(df_frecuencias.set_index('Palabra'))
                    
                    # Muestra la tabla
                    st.dataframe(df_frecuencias, use_container_width=True)
                else:
                    st.info("No se detectaron palabras clave después del preprocesamiento.")

# Crea una instancia para ser importada en app.py
nlp_view = NLPView()