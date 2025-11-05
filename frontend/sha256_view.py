import streamlit as st
from frontend import sha256

def render():
    st.header("Hashing con SHA-256")
    st.markdown("""
    **Definición:** SHA-256 (Secure Hash Algorithm 256-bit) es una función de hash criptográfica que produce un valor de hash de 256 bits (32 bytes). Es un proceso unidireccional e irreversible, fundamental para la seguridad e integridad de los datos.
    """)
    
    text_to_hash = st.text_area("Introduce el texto que deseas procesar:")
    
    if st.button("Calcular Hash SHA-256"):
        if not text_to_hash:
            st.warning("Por favor, introduce un texto para procesar.")
        else:
            hashed_text = sha256.hash_text(text_to_hash)
            st.success(f"El hash SHA-256 del texto es:")
            st.code(hashed_text, language="")