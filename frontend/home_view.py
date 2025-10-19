import streamlit as st

def render():
    # Imagen superior
    st.image("assets/cintillo.png", use_container_width=True)
    # Título principal
    st.title("""
        Calculadora de Ciencia de Datos
    """)
    
    # Subtítulo
    st.subheader("Bienvenido 👋")

    # Descripción general
    st.write("""
        Esta calculadora es un proyecto que integra múltiples módulos de 
        matemáticas, estadística, ciencia de datos e inteligencia artificial.  

        Puedes navegar entre los distintos módulos desde el menú lateral (a la izquierda).  
        Cada módulo incluye **operaciones específicas** con su propia vista e interfaz.
    """)
    
    # Sección de módulos disponibles
    st.markdown("""
        ### Módulos disponibles
    """)
    st.markdown("""
    - 🧮 Aritmética
    - 📊 Visualizador de Datos
    """)
    
    # Nota final
    st.info("""
        Selecciona un módulo en el menú lateral para comenzar.
    """)
