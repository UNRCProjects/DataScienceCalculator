import heapq

def dijkstra(graph, start, end):
    """
    Implementación del algoritmo de Dijkstra
    Retorna: (distancia, camino, pasos)
    """
    # Inicialización
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    visited = set()
    priority_queue = [(0, start)]
    steps = []
    
    steps.append({
        'paso': 0,
        'accion': f"Inicialización: Distancia desde nodo {start} = 0, todas las demás = ∞"
    })
    
    step_count = 0
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        step_count += 1
        
        steps.append({
            'paso': step_count,
            'accion': f"Visitando nodo {current_node} (distancia actual: {current_distance})"
        })
        
        # Si llegamos al nodo destino, podemos terminar
        if current_node == end:
            break
        
        # Revisar vecinos
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in visited:
                new_distance = current_distance + weight
                
                if new_distance < distances[neighbor]:
                    old_dist = distances[neighbor]
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))
                    
                    steps.append({
                        'paso': step_count,
                        'accion': f"  → Actualizar nodo {neighbor}: {old_dist if old_dist != float('infinity') else '∞'} → {new_distance} (vía nodo {current_node})"
                    })
    
    # Reconstruir el camino
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    
    if distances[end] == float('infinity'):
        return float('infinity'), [], steps
    
    return distances[end], path, steps

def add_connection(graph, from_node, to_node, weight):
    """Agregar conexión bidireccional al grafo"""
    if from_node not in graph:
        graph[from_node] = []
    if to_node not in graph:
        graph[to_node] = []
    
    # Agregar en ambas direcciones
    graph[from_node].append((to_node, weight))
    graph[to_node].append((from_node, weight))
    
    return graph

def remove_connection(graph, from_node, to_node):
    """Eliminar conexión bidireccional del grafo"""
    if from_node in graph:
        graph[from_node] = [(n, w) for n, w in graph[from_node] if n != to_node]
    if to_node in graph:
        graph[to_node] = [(n, w) for n, w in graph[to_node] if n != from_node]
    return graph

def get_all_nodes(graph):
    """Obtener lista de todos los nodos ordenados"""
    return sorted(graph.keys(), key=lambda x: int(x) if x.isdigit() else x)
