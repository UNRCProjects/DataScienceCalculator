import streamlit as st
from backend.criptografia import caesar_encrypt, caesar_decrypt

def render():
    st.title("Cifrado Caesar")
    
    st.markdown("""
    ### Descripción
    El cifrado César es una de las técnicas de cifrado más simples y conocidas. 
    Es un tipo de cifrado por sustitución en el que cada letra del texto plano 
    se reemplaza por una letra que se encuentra un número fijo de posiciones 
    más adelante en el alfabeto.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        texto_cifrar = st.text_input("Mensaje a cifrar", value="HELLO")
        desplazamiento_cifrar = st.slider("Desplazamiento para cifrar", 1, 25, 3, key="desp_cif")
        if st.button("Cifrar"):
            try:
                resultado = caesar_encrypt(texto_cifrar, int(desplazamiento_cifrar))
                st.success("Mensaje cifrado:")
                st.code(resultado)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        texto_descifrar = st.text_input("Mensaje a descifrar", value="", key="descifrar")
        desplazamiento_descifrar = st.slider("Desplazamiento para descifrar", 1, 25, 3, key="desp_desc")
        if st.button("Descifrar"):
            try:
                resultado = caesar_decrypt(texto_descifrar, int(desplazamiento_descifrar))
                st.success("Mensaje descifrado:")
                st.code(resultado)
            except Exception as e:
                st.error(f"Error: {str(e)}")
