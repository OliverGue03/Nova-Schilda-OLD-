# F3: Lieferkapazitäten

from collections import deque

def build_capacity_graph(network):
    # Erstellt leeren Kapazitätsgraph
    capacity_graph = {}
    # Initialisiere Knoten im Kapazitätsgraph
    for node_id in network.nodes:
        capacity_graph[node_id] = {}
    # Füge Kanten mit Kapazitäten hinzu
    for from_id, to_id, edge_data in network.all_edges:
        # Nur non-restricted Kanten berücksichtigen
        if not edge_data.get('restricted', False):
            # Kapazität der Kante hinzufügen
            capacity = edge_data.get('capacity', 0)
            capacity_graph[from_id][to_id] = capacity
    
    return capacity_graph


def bfs_find_path(capacity_graph, residual, source, sink, parent):
    # Initialisiere besuchte Knoten und Warteschlange
    visited = set([source])
    queue = deque([source])
    # BFS Schleife
    while queue:
        # Erster Knoten aus der Warteschlange nehmen
        u = queue.popleft()
        # Alle Nachbarn durchgehen
        for v in capacity_graph.get(u, {}):
            # Residualkapazität berechnen
            residual_capacity = capacity_graph[u][v] - residual[u][v]

            if v not in visited and residual_capacity > 0:
                # Knoten als besucht markieren und Vorgänger setzen
                visited.add(v)
                parent[v] = u
                # Wenn Sink erreicht, Pfad gefunden
                if v == sink:
                    return True
                
                # Knoten zur Warteschlange hinzufügen
                queue.append(v)

    # Kein Pfad gefunden
    return False


def edmonds_karp(capacity_graph, source, sink):
    # Residualgraph
    residual = {}
    # Initialisiere Residualgraph
    for u in capacity_graph:
        residual[u] = {}
        for v in capacity_graph[u]:
            residual[u][v] = 0
    
    # Maximaler Fluss initialisieren
    max_flow = 0
    parent = {}
    
    # Augmenting paths finden
    while bfs_find_path(capacity_graph, residual, source, sink, parent):
        # Pfadfluss auf unendlich setzen
        path_flow = float('inf')
        s = sink
        # Solange wir nicht am Quellknoten sind, den minimalen Kapazitätswert finden
        while s != source:
            # u ist der Vorgänger von s
            u = parent[s]
            # Pfadfluss aktualisieren (entweder aktueller Pfadfluss oder Kapazität der Kante im Residualgraph)
            path_flow = min(path_flow, capacity_graph[u][s] - residual[u][s])
            s = u
        
        # Flow aktualisieren
        max_flow += path_flow
        v = sink
        
        # Rückwärtskanten im Residualgraph aktualisieren
        while v != source:
            u = parent[v]
            # Residualkapazität aktualisieren
            residual[u][v] += path_flow
            # Ist Kante nicht im Residualgraph, initialisiere sie
            if v not in residual:
                residual[v] = {}
            if u not in residual[v]:
                residual[v][u] = 0
            # Rückwärtskante aktualisieren
            residual[v][u] -= path_flow
            v = u
        
        parent = {}
    
    return max_flow, residual


def calculate_delivery_capacity(network, hub_id, delivery_area):

    capacity_graph = build_capacity_graph(network)
    
    # Supersink hinzufügen
    supersink = "__SUPERSINK__"
    # Kapazitätsgraph um Supersink erweitern
    capacity_graph[supersink] = {}
    
    # Füge Kanten von allen Delivery-Punkten im Liefergebiet zum Supersink hinzu mit Kantengewicht unendlich
    for delivery_id in delivery_area:
        if delivery_id in network.nodes:
            capacity_graph[delivery_id][supersink] = float('inf')
    
    # Führe Edmonds-Karp Algorithmus aus
    max_flow, residual = edmonds_karp(capacity_graph, hub_id, supersink)
    
    # Verwendete Kanten extrahieren
    used_edges = []
    # Durchlaufe Residualgraph
    for from_id in residual:
        for to_id in residual[from_id]:
            # Wenn Fluss > 0 und Ziel ist nicht Supersink, dann Kante als verwendet markieren
            if residual[from_id][to_id] > 0 and to_id != supersink:
                edge = {
                    'from': from_id,
                    'to': to_id,
                    'flow': residual[from_id][to_id],
                    'capacity': capacity_graph.get(from_id, {}).get(to_id, 0)
                }
                used_edges.append(edge)
    
    return {
        'hub_id': hub_id,
        'delivery_area': delivery_area,
        'max_capacity': int(max_flow) if max_flow != float('inf') else max_flow,
        'used_edges': used_edges,
    }


"""
Beispiel Eingabe:
build_capacity_graph(myDroneNetwork)
Beispiel Ausgabe:
{
    'hub_1': {'node_5': 20, 'node_6': 15},
    'node_5': {'delivery_1': 10, 'delivery_2': 10},
    'node_6': {'delivery_3': 10},
    'delivery_1': {},
    'delivery_2': {},
    'delivery_3': {}
}

Beispiel Eingabe:
edmonds_karp(capacity_graph, 'hub_1', '__SUPERSINK__')
Beispiel Ausgabe:
(25, {
    'hub_1': {'node_5': 15, 'node_6': 10},
    'node_5': {'delivery_1': 10, 'delivery_2': 5},
    'node_6': {'delivery_3': 10},
    'delivery_1': {'__SUPERSINK__': -10},
    'delivery_2': {'__SUPERSINK__': -5},
    'delivery_3': {'__SUPERSINK__': -10},
    '__SUPERSINK__': {}
})

Beispiel Eingabe:
calculate_delivery_capacity(myDroneNetwork, 'hub_1', ['delivery_1', 'delivery_2', 'delivery_3'])
Beispiel Ausgabe:
{
    'hub_id': 'hub_1',
    'delivery_area': ['delivery_1', 'delivery_2', 'delivery_3'],
    'max_capacity': 25,
    'used_edges': [
        {'from': 'hub_1', 'to': 'node_5', 'flow': 15, 'capacity': 20},
        {'from': 'node_5', 'to': 'delivery_1', 'flow': 10, 'capacity': 10},
        {'from': 'node_5', 'to': 'delivery_2', 'flow': 5, 'capacity': 10},
        {'from': 'hub_1', 'to': 'node_6', 'flow': 10, 'capacity': 15},
        {'from': 'node_6', 'to': 'delivery_3', 'flow': 10, 'capacity': 10}
    ]
}
"""