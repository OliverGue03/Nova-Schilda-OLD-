# B3: Drohnennetzwerk erweitern und anpassen

def add_charging_station(network, station_id, x, y, name=None):
    # Fügt Ladestation hinzu
    if station_id in network.nodes:
        return False
    
    node_data = {
        'id': station_id,
        'type': 'charging',
        'x': x,
        'y': y,
        'name': name or f"Charging Station {station_id}"
    }
    
    network.add_node(station_id, node_data)
    return True


def add_delivery_point(network, point_id, x, y, name=None):
    # Fügt Auslieferungspunkt hinzu
    if point_id in network.nodes:
        return False
    
    node_data = {
        'id': point_id,
        'type': 'delivery',
        'x': x,
        'y': y,
        'name': name or f"Delivery Point {point_id}"
    }
    
    network.add_node(point_id, node_data)
    return True


def add_hub(network, hub_id, x, y, name=None):
    # Fügt Hub hinzu, wenn Hub-ID nicht vorhanden
    if hub_id in network.nodes:
        return False
    
    node_data = {
        'id': hub_id,
        'type': 'hub',
        'x': x,
        'y': y,
        'name': name or f"Hub {hub_id}"
    }
    
    network.add_node(hub_id, node_data)
    return True


def add_flight_corridor(network, from_id, to_id, energy_cost, capacity,
                       distance=None, bidirectional=False):
    # Fügt Flugkorridor hinzu
    if from_id not in network.nodes or to_id not in network.nodes:
        return False
    
    edge_data = {
        'energy_cost': energy_cost,
        'capacity': capacity,
        'bidirectional': bidirectional,
        'restricted': False
    }
    
    if distance is not None:
        edge_data['distance'] = distance
    
    network.add_edge(from_id, to_id, edge_data)
    return True


def modify_corridor_energy(network, from_id, to_id, new_energy):
    # Ändert Energieverbrauch einer Kante
    network.update_edge_energy(from_id, to_id, new_energy)
    return True


def modify_corridor_capacity(network, from_id, to_id, new_capacity):
    # Ändert Kapazität einer Kante
    network.update_edge_capacity(from_id, to_id, new_capacity)
    return True


"""
Beispiel Eingabe:
add_charging_station(myDroneNetwork, 'CS1', 10, 20, name='Central Charging')
Beispiel Ausgabe:
True

Beispiel Eingabe:
add_flight_corridor(myDroneNetwork, 'A', 'B', energy_cost=5, capacity=10, bidirectional=True)
Beispiel Ausgabe:
True

Beispiel Eingabe:
modify_corridor_capacity(myDroneNetwork, 'A', 'B', new_capacity=15)
Beispiel Ausgabe:
True

Beispiel Eingabe:
modify_corridor_energy(myDroneNetwork, 'A', 'B', new_energy=7)
Beispiel Ausgabe:
True
"""