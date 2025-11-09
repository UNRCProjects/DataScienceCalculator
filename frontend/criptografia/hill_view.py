import streamlit as st
import numpy as np
from backend.criptografia import hill_encrypt, hill_decrypt

def render():
    st.title("🔢 Cifrado Hill")
    
    st.markdown("""
    ### Descripción
    El cifrado Hill es un cifrado poligráfico basado en álgebra lineal. 
    Cada letra se reemplaza por un número modular y se utilizan matrices 
    para transformar bloques de texto.
    """)

    st.subheader("Matriz Clave (2x2)")
    col1, col2 = st.columns(2)
    
    with col1:
        a11 = st.number_input("a11", value=2)
        a12 = st.number_input("a12", value=1)
    with col2:
        a21 = st.number_input("a21", value=3)
        a22 = st.number_input("a22", value=4)
    
    key_matrix = np.array([[a11, a12], [a21, a22]])
    mensaje = st.text_input("Mensaje", "HELLO")
    
    if st.button("Cifrar/Descifrar"):
        try:
            encrypted = hill_encrypt(mensaje, key_matrix)
            decrypted = hill_decrypt(encrypted, key_matrix)
            
            st.success("Resultado:")
            st.write("Mensaje cifrado:", encrypted)
            st.write("Mensaje descifrado:", decrypted)
        except Exception as e:
            st.error(f"Error: {str(e)}")
