# F4: Ausfallsicherheitsanalyse

import calculate_delivery_capacity as calc_cap


def find_bridges(network):
    # Zeitstempel für Entdeckungszeiten
    time = [0]
    visited = set()
    # Entdeckungs- und Niedrigstwerte
    disc = {}
    low = {}
    # Elternknoten im DFS-Baum
    parent = {}
    bridges = []

    # Tiefensuche zur Brückenerkennung
    def dfs_bridges(u):
        # Startknoten als besucht markieren und Zeiten setzen
        visited.add(u)
        disc[u] = time[0]
        low[u] = time[0]
        time[0] += 1
        
        neighbors = network.get_neighbors(u)
        # Nachbarn durchlaufen
        for v, _ in neighbors:
            # Ist Nachbar nicht besucht
            if v not in visited:
                # u als Elternteil von v setzen
                parent[v] = u
                # v rekursiv besuchen
                dfs_bridges(v)
                
                # Niedrigstwert von u aktualisieren (entweder eigener oder von v)
                low[u] = min(low[u], low[v])
                
                # Brücke gefunden, wenn Niedrigstwert von v größer ist als Entdeckungszeit von u
                if low[v] > disc[u]:
                    bridges.append((u, v))
            
            # Ist Nachbar besucht und nicht der Elternknoten
            elif v != parent.get(u):
                # Niedrigstwert von u aktualisieren
                low[u] = min(low[u], disc[v])
    
    # Alle Knoten durchlaufen
    for node in network.nodes:
        if node not in visited:
            dfs_bridges(node)
    
    return bridges


def find_bottlenecks(network):
    # Hubs finden
    hubs = [node_id for node_id, data in network.nodes.items() 
            if data.get('type') == 'hub']
    
    # Wenn kein Hub gefunden, leere Liste zurückgeben 
    if not hubs:
        return []
    
    # Wähle erstes Hub als Startknoten
    hub_id = hubs[0]
    
    # Alle Delivery-Punkte finden
    deliveries = [node_id for node_id, data in network.nodes.items() 
                 if data.get('type') == 'delivery']
    
    # Wenn keine Delivery-Punkte, leere Liste zurückgeben
    if not deliveries:
        return []
    
    # Kapazitätsgraph erstellen
    capacity_graph = calc_cap.build_capacity_graph(network)
    
    # Supersink für alle Delivery-Punkte
    supersink = "__SUPERSINK__"
    # Kapazitätsgraph um Supersink erweitern
    capacity_graph[supersink] = {}
    # Füge Kanten von allen Delivery-Punkten im Liefergebiet zum Supersink hinzu mit Kantengewicht unendlich
    for delivery_id in deliveries:
        if delivery_id in network.nodes:
            capacity_graph[delivery_id][supersink] = float('inf')
    
    # Führe Edmonds-Karp Algorithmus aus und erhalte Residualgraph
        _, residual = calc_cap.edmonds_karp(capacity_graph, hub_id, supersink)
    
    # Erreichbare Knoten von hub_id im Residualgraph finden
    reachable = set()
    # Stack für DFS
    stack = [hub_id]
    reachable.add(hub_id)
    
    # DFS im Residualgraph
    while stack:
        u = stack.pop()
        for v in capacity_graph.get(u, {}):
            residual_capacity = capacity_graph[u][v] - residual[u].get(v, 0)
            if v not in reachable and residual_capacity > 0:
                reachable.add(v)
                stack.append(v)
    
    # Bottlenecks identifizieren
    bottlenecks = []
    # Kanten von erreichbaren zu nicht erreichbaren Knoten im Kapazitätsgraphen prüfen
    for u in reachable:
        for v in capacity_graph.get(u, {}):
            if v not in reachable and v != supersink:
                capacity = capacity_graph[u][v]
                bottlenecks.append((u, v, capacity))
    
    return bottlenecks


def analyze_network_resilience(network):
    # Führt Ausfallsicherheitsanalyse durch
    bridges = find_bridges(network)
    bottlenecks = find_bottlenecks(network)
    
    return {
        'bridges': bridges,
        'bottlenecks': bottlenecks
    }


"""
Eingabe Beispiel:
find_bridges(myDroneNetwork)
Ausgabe Beispiel:
[('node_2', 'node_5'), ('node_3', 'node_7')]

Eingabe Beispiel:
find_bottlenecks(myDroneNetwork)
Ausgabe Beispiel:
[('hub_1', 'node_4', 50), ('node_6', 'delivery_3', 30)]

Eingabe Beispiel:
analyze_network_resilience(myDroneNetwork)
Ausgabe Beispiel:
{
    'bridges': [('node_2', 'node_5'), ('node_3', 'node_7')],
    'bottlenecks': [('hub_1', 'node_4', 50), ('node_6', 'delivery_3', 30)]
}

"""