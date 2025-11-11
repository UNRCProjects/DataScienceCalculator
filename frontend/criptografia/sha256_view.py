import streamlit as st
from backend.criptografia import sha256_hash

def render():
    st.header("SHA-256 Hash")
    st.markdown("""
    El algoritmo SHA-256 genera un hash único de 256 bits para un mensaje de texto dado. Es ampliamente utilizado en criptografía y seguridad informática.
    """)
    texto = st.text_area("Texto a hashear", value="")
    if st.button("Calcular SHA-256"):
        hash_result = sha256_hash(texto)
        st.code(hash_result)
