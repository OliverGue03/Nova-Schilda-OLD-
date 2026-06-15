# F1: Erreichbarkeit prüfen

from collections import deque

# BFS zur Überprüfung der Erreichbarkeit aller Knoten von einem Hub aus
def check_reachability_bfs(network, hub_id):
    # Wenn Hub nicht existiert, Rückgabe False und leere Sets
    if hub_id not in network.nodes:
        return False, set(), set()
    
    # BFS Initialisierung
    visited = set()
    # Warteschlange und Visited beinhalten HUB
    queue = deque([hub_id])
    visited.add(hub_id)
    # Alle erreichbaren Knoten sammeln
    while queue:
        # Erster Knoten aus der Warteschlange nehmen
        current = queue.popleft()
        # Alle Nachbarn durchgehen von aktuellem Knoten
        for neighbor, _ in network.get_neighbors(current):
            # Wenn Nachbar noch nicht besucht, besuche ihn
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    # Delivery-Punkte finden für den Vergleich
    delivery_points = set()
    for node_id, data in network.nodes.items():
        if data.get('type') == 'delivery':
            delivery_points.add(node_id)
    
    unreachable = delivery_points - visited
    # Wenn alle erreichbar sind, hat unreachable den Wert 0
    all_reachable = len(unreachable) == 0
    
    return all_reachable, visited, unreachable


def find_all_hubs(network):
    # Findet alle Drohnen-Hubs und gibt diese zurück
    hubs = []
    for node_id, data in network.nodes.items():
        if data.get('type') == 'hub':
            hubs.append(node_id)
    return hubs


def get_reachability_report(network, hub_id):
    # Erstellt einen ausführlichen Erreichbarkeitsbericht für ein ausgewähltes Hub
    all_reachable, visited, unreachable = check_reachability_bfs(network, hub_id)
    
    # Zähle alle Delivery-Punkte im Netzwerk --> wenn type == 'delivery', dann +1
    total_delivery = sum(1 for data in network.nodes.values() 
                        if data.get('type') == 'delivery')
    # Anzahl erreichbarer Delivery-Punkte
    reachable_delivery = total_delivery - len(unreachable)
    
    return {
        'hub_id': hub_id,
        'all_reachable': all_reachable,
        'total_nodes_reachable': len(visited),
        'total_delivery_points': total_delivery,
        'reachable_delivery_points': reachable_delivery,
        'unreachable_list': list(unreachable)
    }


"""
Eingabe Beispiel:
find_all_hubs(myDroneNetwork)
Ausgabe Beispiel:
['hub_1', 'hub_2', 'hub_3']

Eingabe Beispiel:
check_reachability_bfs(myDroneNetwork, 'hub_1')
Ausgabe Beispiel:
(True, ('hub_1', 'delivery_1', 'delivery_2', ...), (empty set))

Eingabe Beispiel:
get_reachability_report(myDroneNetwork, 'hub_1')
Ausgabe Beispiel:
{
    'hub_id': 'hub_1',
    'all_reachable': False,
    'total_nodes_reachable': 15,
    'total_delivery_points': 10,
    'reachable_delivery_points': 7,
    'unreachable_list': ['delivery_5', 'delivery_8', 'delivery_9']
}
"""