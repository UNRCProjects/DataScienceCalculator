import streamlit as st

def render():
    # Imagen superior
    st.image("assets/cintillo.png", width="stretch")
    # Título principal
    st.title("""
        Calculadora de Ciencia de Datos
    """)
    
    # Subtítulo
    st.subheader("Bienvenido!")

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
    st.markdown("""- Áritmetica""")
    st.markdown("""- Criptografía""")
    st.markdown("""- Cálculo Diferencial""")
