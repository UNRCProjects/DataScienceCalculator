import streamlit as st
from frontend.aritmetica import mcd_view, mcm_view, primos_view, coprimos_view
from frontend import home_view
from frontend import autores_view
# Importamos la nueva vista de visualización
from frontend.visualizacion import scatter_view

# Configuración inicial de la app
st.set_page_config(
    page_title="Calculadora Colaborativa",
    page_icon="assets/favicon.ico",
    layout="wide"
)

# --- Definición de las Vistas y Navegación ---
# Estructura para registrar todas las vistas disponibles en la aplicación.
PAGES = {
    "Home": {
        "Principal": home_view.render,
        "Autores": autores_view.render,
    },
    "Visualización": {
        "Gráfico de Dispersión": scatter_view.render,
    }
}

# ====== BARRA LATERAL ======
st.sidebar.image("assets/logo_unrc.png")

# Selección de categoría principal
st.sidebar.title("📂 Navegación")
categoria_seleccionada = st.sidebar.radio("Módulo", list(PAGES.keys()))

# Selección de subopción dentro de la categoría
subopciones = PAGES[categoria_seleccionada]
subopcion_seleccionada = st.sidebar.radio("Operación", list(subopciones.keys()))

# --- Renderizado de la Vista ---
# Se busca la función correspondiente en el diccionario y se ejecuta.
render_function = PAGES[categoria_seleccionada][subopcion_seleccionada]
render_function()

# Sidebar con categorías y subopciones tipo dropdown
with st.sidebar.expander("🏠 Home", expanded=False):
    if st.button("Ir a Home", key="home_btn"):
        st.session_state['categoria'] = "Home"
        st.session_state['subopcion'] = "Principal"
    if st.button("Autores", key="autores_btn"):
        st.session_state['categoria'] = "Autores"

with st.sidebar.expander("🧮 Aritmética"):
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

# Ruteo según selección
categoria = st.session_state['categoria']
subopcion = st.session_state['subopcion']

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
elif categoria == "Autores":
    autores_view.render()

# Footer
st.markdown(
    '''<hr style="margin-top:40px; margin-bottom:10px;">\
    <div style="text-align:center; color: #888; font-size: 0.95em;">
        Universidad Nacional Rosario Castellanos &copy; 2025<br>
        Proyecto Calculadora de Ciencia de Datos
    </div>''', unsafe_allow_html=True)
