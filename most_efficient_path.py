# F2: effiziente Flugrouten

import heapq

# Dijkstra-Algorithmus zur Berechnung des energieeffizientesten Pfads
def dijkstra(network, start, end):
    # Wenn Start- oder Endknoten nicht existieren, unendliche Kosten und leeren Pfad zurückgeben
    if start not in network.nodes or end not in network.nodes:
        return float('inf'), []
    
    # Unendliche Anfangsdistanzen
    distances = {node: float('inf') for node in network.nodes}
    # Startdistantz ist 0
    distances[start] = 0
    
    previous = {node: None for node in network.nodes}
    
    # Priority Queue
    pq = [(0, start)]
    visited = set()
    
    while pq:
        # Aktuelle Distanz und Knoten aus der Priority Queue holen
        current_dist, current = heapq.heappop(pq)
        # Wenn Knoten schon besucht, überspringen
        if current in visited:
            continue
        # Knoten als besucht markieren
        visited.add(current)
        # Wenn Zielknoten erreicht, While-Schleife beenden
        if current == end:
            break
        # Wenn die aktuelle Distanz größer ist als die gespeicherte Distanz, dann überspringen
        if current_dist > distances[current]:
            continue
        
        # Nachbarn prüfen
        for neighbor, edge_data in network.get_neighbors(current, include_blocked=False):
            # Energiekosten der Kante = Kantengewicht
            weight = edge_data.get('energy_cost', float('inf'))
            # Neue Distanz berechnen
            new_dist = distances[current] + weight
            
            # Wenn neue Distanz kleiner ist als gespeicherte Distanz, dann
            if new_dist < distances[neighbor]:
                # Aktuelle Distanz aktualisieren
                distances[neighbor] = new_dist
                # Vorgänger des Nachbarn aktualisieren
                previous[neighbor] = current
                # Nachbarn mit neuer Distanz in die Priority Queue einfügen
                heapq.heappush(pq, (new_dist, neighbor))
    
    # Pfad rekonstruieren
    path = []
    # Startknoten des Pfads ist der Endknoten
    current = end
    # Pfad zurückverfolgen bis zum Startknoten
    while current is not None:
        path.append(current)
        current = previous[current]
    # Pfad umkehren, da er rückwärts aufgebaut wurde
    path.reverse()
    
    # Sollte der Pfad nicht mit dem Startknoten beginnen oder leer sein, gibt es keinen gültigen Pfad
    if len(path) == 0 or path[0] != start:
        return float('inf'), []
    
    return distances[end], path


def find_route(network, hub_id, delivery_id):
    total_energy, path = dijkstra(network, hub_id, delivery_id)
    # Wenn kein Pfad gefunden wurde
    if total_energy == float('inf'):
        return {
            'success': False,
            'total_energy': None,
            'total_distance': None,
            'path': []
        }
    
    # Deklarierung von Energiekosten und Distanz
    total_distance = 0
    
    # Gesamtdistanz berechnen
    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        
        for neighbor, edge_data in network.get_neighbors(from_node, include_blocked=True):
            if neighbor == to_node:
                total_distance += edge_data.get('distance', 0)
                break
    
    return {
        'success': True,
        'path': path,
        'total_energy': total_energy,
        'total_distance': total_distance
    }

"""
Eingabe Beispiel:
dijkstra(myDroneNetwork, 'hub_1', 'delivery_5')
Ausgabe Beispiel:
(150.0, ['hub_1', 'node_3', 'delivery_5'])

Eingabe Beispiel:
find_route(myDroneNetwork, 'hub_1', 'delivery_5')
Ausgabe Beispiel:
{
    'success': True,
    'path': ['hub_1', 'node_3', 'delivery_5'],
    'total_energy': 150.0,
    'total_distance': 12.5
}
"""