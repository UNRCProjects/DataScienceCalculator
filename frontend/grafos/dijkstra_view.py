import streamlit as st
import pandas as pd
from backend.grafos.dijkstra import dijkstra, add_connection, remove_connection, get_all_nodes

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Dijkstra",
    page_icon="🗺️",
    layout="wide"
)

# Inicializar el estado de la sesión
if 'graph' not in st.session_state:
    # Grafo de ejemplo
    st.session_state.graph = {
        '1': [('2', 2), ('3', 4)],
        '2': [('1', 2), ('3', 1), ('4', 7)],
        '3': [('1', 4), ('2', 1), ('4', 3), ('5', 5)],
        '4': [('2', 7), ('3', 3), ('5', 2), ('6', 6)],
        '5': [('3', 5), ('4', 2), ('6', 4), ('7', 3)],
        '6': [('4', 6), ('5', 4), ('7', 2), ('8', 5)],
        '7': [('5', 3), ('6', 2), ('8', 4)],
        '8': [('6', 5), ('7', 4)]
    }

# Título principal
st.title("🗺️ Calculadora del Algoritmo de Dijkstra")
st.markdown("---")

# Información
with st.expander("ℹ️ ¿Qué es el Algoritmo de Dijkstra?"):
    st.markdown("""
    El **Algoritmo de Dijkstra** es un algoritmo de búsqueda de caminos que encuentra la ruta más corta 
    entre nodos en un grafo con pesos no negativos.
    
    **Pasos del algoritmo:**
    1. Se inicializan todas las distancias a infinito, excepto el nodo inicial (0)
    2. Se selecciona el nodo no visitado con la menor distancia
    3. Se actualizan las distancias de sus vecinos si se encuentra un camino más corto
    4. Se marca el nodo como visitado y se repite
    5. Se reconstruye el camino desde el inicio hasta el destino
    """)

# Layout en columnas
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Editor del Grafo")
    
    # Editor de grafo
    with st.expander("➕ Agregar Nueva Conexión", expanded=False):
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            from_node = st.text_input("Desde Nodo", key="from_node", placeholder="Ej: 1")
        with col_b:
            to_node = st.text_input("Hasta Nodo", key="to_node", placeholder="Ej: 2")
        with col_c:
            weight = st.number_input("Peso", min_value=0.0, step=0.1, key="weight")
        
        if st.button("➕ Agregar Conexión", use_container_width=True):
            if from_node and to_node and weight > 0:
                st.session_state.graph = add_connection(
                    st.session_state.graph, 
                    from_node, 
                    to_node, 
                    weight
                )
                st.success(f"✅ Conexión agregada: {from_node} ↔ {to_node} (peso: {weight})")
                st.rerun()
            else:
                st.error("⚠️ Por favor completa todos los campos correctamente")
    
    # Botones de control
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Restaurar Ejemplo", use_container_width=True):
            st.session_state.graph = {
                '1': [('2', 2), ('3', 4)],
                '2': [('1', 2), ('3', 1), ('4', 7)],
                '3': [('1', 4), ('2', 1), ('4', 3), ('5', 5)],
                '4': [('2', 7), ('3', 3), ('5', 2), ('6', 6)],
                '5': [('3', 5), ('4', 2), ('6', 4), ('7', 3)],
                '6': [('4', 6), ('5', 4), ('7', 2), ('8', 5)],
                '7': [('5', 3), ('6', 2), ('8', 4)],
                '8': [('6', 5), ('7', 4)]
            }
            st.rerun()
    
    with col_btn2:
        if st.button("🗑️ Limpiar Todo", use_container_width=True):
            st.session_state.graph = {}
            st.rerun()
    
    st.markdown("---")
    
    # Visualización del grafo actual
    st.subheader(f"🔍 Grafo Actual ({len(st.session_state.graph)} nodos)")
    
    if not st.session_state.graph:
        st.info("No hay conexiones. Agrega algunas usando el editor arriba.")
    else:
        # Crear tabla de conexiones
        connections_data = []
        for node in get_all_nodes(st.session_state.graph):
            neighbors = st.session_state.graph[node]
            if neighbors:
                neighbor_str = ", ".join([f"{n} (peso: {w})" for n, w in neighbors])
                connections_data.append({
                    "Nodo": node,
                    "Conectado con": neighbor_str
                })
            else:
                connections_data.append({
                    "Nodo": node,
                    "Conectado con": "Sin conexiones"
                })
        
        df = pd.DataFrame(connections_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.header("🧮 Calculadora de Rutas")
    
    if st.session_state.graph:
        nodes = get_all_nodes(st.session_state.graph)
        
        col_start, col_end = st.columns(2)
        
        with col_start:
            start_node = st.selectbox("Nodo Inicial", nodes, key="start_select")
        
        with col_end:
            end_node = st.selectbox("Nodo Final", nodes, index=min(len(nodes)-1, 1), key="end_select")
        
        if st.button("🚀 Calcular Ruta Más Corta", type="primary", use_container_width=True):
            if start_node and end_node:
                distance, path, steps = dijkstra(st.session_state.graph, start_node, end_node)
                
                st.markdown("---")
                
                if distance == float('infinity'):
                    st.error(f"❌ No hay camino disponible entre los nodos {start_node} y {end_node}")
                else:
                    # Resultado principal
                    st.success("✅ Ruta encontrada")
                    
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.metric("Distancia Total", f"{distance}")
                    with col_res2:
                        st.metric("Nodos en el Camino", len(path))
                    
                    st.info(f"**Camino:** {' → '.join(path)}")
                    
                    # Pasos del algoritmo
                    st.markdown("---")
                    st.subheader("📋 Proceso del Algoritmo (Paso a Paso)")
                    
                    # Crear DataFrame de pasos
                    steps_df = pd.DataFrame(steps)
                    
                    # Mostrar en contenedor con scroll
                    with st.container():
                        st.markdown(
                            """
                            <div style='height:400px; overflow-y:auto; border:1px solid #ccc; padding:10px; border-radius:10px;'>
                            """,
                            unsafe_allow_html=True
                            )
                        for i, step in enumerate(steps):
                            if "Inicialización" in step['accion']:
                                st.info(f"**Paso {step['paso']}:** {step['accion']}")
                            elif "Visitando" in step['accion']:
                                st.warning(f"**Paso {step['paso']}:** {step['accion']}")
                            else:
                                st.success(step['accion'])
                    
                    # Opción de descargar pasos
                    csv = steps_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar Pasos en CSV",
                        data=csv,
                        file_name=f"dijkstra_{start_node}_to_{end_node}.csv",
                        mime="text/csv"
                    )
    else:
        st.warning("⚠️ Primero agrega conexiones al grafo usando el editor de la izquierda.")

# Sección adicional: Calcular desde un nodo a todos
st.markdown("---")
st.header("🌐 Calcular Rutas desde un Nodo a Todos los Demás")

if st.session_state.graph:
    nodes = get_all_nodes(st.session_state.graph)
    
    col_source, col_calc = st.columns([3, 1])
    
    with col_source:
        source_node = st.selectbox("Selecciona el nodo origen", nodes, key="source_all")
    
    with col_calc:
        st.write("")  # Espaciador
        st.write("")  # Espaciador
        calc_all = st.button("Calcular Todas", use_container_width=True)
    
    if calc_all:
        results_data = []
        
        for target_node in nodes:
            if target_node != source_node:
                distance, path, _ = dijkstra(st.session_state.graph, source_node, target_node)
                
                if distance != float('infinity'):
                    results_data.append({
                        "Destino": target_node,
                        "Distancia": distance,
                        "Camino": " → ".join(path)
                    })
                else:
                    results_data.append({
                        "Destino": target_node,
                        "Distancia": "∞",
                        "Camino": "Sin camino"
                    })
        
        if results_data:
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            # Descargar resultados
            csv_all = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar Todos los Resultados",
                data=csv_all,
                file_name=f"dijkstra_from_{source_node}_all.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>💡 Desarrollado para el estudio del Algoritmo de Dijkstra</p>
    <p>Creado con Python y Streamlit</p>
</div>
""", unsafe_allow_html=True)