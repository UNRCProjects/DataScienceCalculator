import streamlit as st
from frontend.combinatoria import factorial_view, permutaciones_view, combinaciones_view, probabilidad_basica_view, distribucion_binomial_view
from frontend import home_view
from frontend import autores_view

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

# ====== BARRA LATERAL ======
# st.sidebar.title("📂 Navegación")
st.sidebar.image("assets/logo_unrc.png")

# Sidebar con categorías y subopciones tipo dropdown
with st.sidebar.expander("🏠 Home", expanded=False):
    if st.button("Ir a Home", key="home_btn"):
        st.session_state['categoria'] = "Home"
        st.session_state['subopcion'] = "Principal"
    if st.button("Autores", key="autores_btn"):
        st.session_state['categoria'] = "Autores"

with st.sidebar.expander("📊 Combinatoria y Probabilidad"):
    if st.button("Factorial", key="factorial_btn"):
        st.session_state['categoria'] = "Combinatoria"
        st.session_state['subopcion'] = "Factorial"
    if st.button("Permutaciones", key="permutaciones_btn"):
        st.session_state['categoria'] = "Combinatoria"
        st.session_state['subopcion'] = "Permutaciones"
    if st.button("Combinaciones", key="combinaciones_btn"):
        st.session_state['categoria'] = "Combinatoria"
        st.session_state['subopcion'] = "Combinaciones"
    if st.button("Probabilidad Básica", key="probabilidad_basica_btn"):
        st.session_state['categoria'] = "Combinatoria"
        st.session_state['subopcion'] = "Probabilidad Básica"
    if st.button("Distribución Binomial", key="distribucion_binomial_btn"):
        st.session_state['categoria'] = "Combinatoria"
        st.session_state['subopcion'] = "Distribución Binomial"


# Ruteo según selección
categoria = st.session_state['categoria']
subopcion = st.session_state['subopcion']

if categoria == "Home":
    home_view.render()
elif categoria == "Combinatoria" and subopcion == "Factorial":
    factorial_view.render()
elif categoria == "Combinatoria" and subopcion == "Permutaciones":
    permutaciones_view.render()
elif categoria == "Combinatoria" and subopcion == "Combinaciones":
    combinaciones_view.render()
elif categoria == "Combinatoria" and subopcion == "Probabilidad Básica":
    probabilidad_basica_view.render()
elif categoria == "Combinatoria" and subopcion == "Distribución Binomial":
    distribucion_binomial_view.render()
elif categoria == "Autores":
    autores_view.render()

# Footer
st.markdown(
    '''<hr style="margin-top:40px; margin-bottom:10px;">\
    <div style="text-align:center; color: #888; font-size: 0.95em;">
        Universidad Nacional Rosario Castellanos &copy; 2025<br>
        Proyecto Calculadora de Ciencia de Datos
    </div>''', unsafe_allow_html=True)
