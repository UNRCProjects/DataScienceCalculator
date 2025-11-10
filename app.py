import streamlit as st
from frontend import home_view, autores_view
from frontend.aritmetica import mcd_view, mcm_view, primos_view, coprimos_view
from frontend.criptografia import sha256_view, caesar_view, hill_view
from frontend.calculo_diferencial import derivadas_view

# Configuración inicial de la app
st.set_page_config(
    page_title="Calculadora Colaborativa",
    page_icon="assets/favicon.ico",
    layout="wide"
)

# Inicializar session_state si no existe
if 'categoria' not in st.session_state:
    st.session_state['categoria'] = 'Home'
if 'subopcion' not in st.session_state:
    st.session_state['subopcion'] = 'Principal'
if 'calculo_diferencial_opcion' not in st.session_state:
     st.session_state['calculo_diferencial_opcion'] = 'Derivadas'

# ====== BARRA LATERAL ======
# st.sidebar.title("📂 Navegación")
st.sidebar.image("assets/logo_unrc.png")

# Sidebar con categorías y subopciones tipo dropdown
with st.sidebar.expander("Home", expanded=False):
    if st.button("Ir a Home", key="home_btn"):
        st.session_state['categoria'] = "Home"
        st.session_state['subopcion'] = "Principal"
    if st.button("Autores", key="autores_btn"):
        st.session_state['categoria'] = "Autores"

with st.sidebar.expander("Aritmética"):
    if st.button("Máximo Común Divisor (MCD)", key="mcd_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "MCD"
    if st.button("Mínimo Común Multiplo (MCM)", key="mcm_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "MCM"
    if st.button("Número primo", key="primos_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "Primos"
    if st.button("Números coprimos", key="coprimos_btn"):
        st.session_state['categoria'] = "Aritmética"
        st.session_state['subopcion'] = "Coprimos"

with st.sidebar.expander("Cálculo Diferencial"):
    if st.button("Derivadas", key="derivadas_btn"):
        st.session_state['categoria'] = "Cálculo Diferencial"
        st.session_state['calculo_diferencial_opcion'] = "Derivadas"

with st.sidebar.expander("Cifrado"):
    if st.button("Cifrado SHA256", key="sha256_btn"):
        st.session_state['categoria'] = "Cifrado"
        st.session_state['subopcion'] = "SHA256"
    if st.button("Cifrado Caesar", key="caesar_btn"):
        st.session_state['categoria'] = "Cifrado"
        st.session_state['subopcion'] = "César"
    if st.button("Cifrado Hill", key="hill_btn"):
        st.session_state['categoria'] = "Cifrado"
        st.session_state['subopcion'] = "Hill"

# Ruteo según selección
categoria = st.session_state['categoria']
subopcion = st.session_state['subopcion']
calculo_diferencial_opcion = st.session_state.get('calculo_diferencial_opcion', 'Derivadas')

if categoria == "Home":
    home_view.render()
elif categoria == "Aritmética" and subopcion == "MCD":
    mcd_view.render()
elif categoria == "Aritmética" and subopcion == "MCM":
    mcm_view.render()
elif categoria == "Aritmética" and subopcion == "Primos":
    primos_view.render()
elif categoria == "Aritmética" and subopcion == "Coprimos":
    coprimos_view.render()
elif categoria == "Cálculo Diferencial" and calculo_diferencial_opcion == "Derivadas":
     derivadas_view.render()
elif categoria == "Autores":
    autores_view.render()
elif categoria == "Cifrado" and subopcion == "SHA256":
    sha256_view.render()
elif categoria == "Cifrado" and subopcion == "César":
    caesar_view.render()
elif categoria == "Cifrado" and subopcion == "Hill":
    hill_view.render()

# Footer
st.markdown(
    '''<hr style="margin-top:40px; margin-bottom:10px;">\
    <div style="text-align:center; color: #888; font-size: 0.95em;">
        Universidad Nacional Rosario Castellanos &copy; 2025<br>
        Proyecto Calculadora de Ciencia de Datos
    </div>''', unsafe_allow_html=True)
