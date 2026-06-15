# F6: Kommunikationsinfrastruktur


import math
import heapq
import random

# Kürzeste Distanz zwischen zwei Knoten (euklidische Distanz)
def euclidean_distance(x1, y1, x2, y2):
    # Gibt kürzeste Distanz zurück
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def build_station_mst(network):
    # Drohnenstationen finden
    stations = []
    station_coords = {}
    
    # Durchlaufe alle Knoten im Netzwerk
    for node_id, data in network.nodes.items():
        # Liste aller Typen von Stationen
        node_type = data.get('type')
        # Wenn Station eine Drohnenstation ist, dann Koordinaten herausfinden
        if node_type in ['hub', 'charging', 'relay']:
            x = data.get('x')
            y = data.get('y')
            # Wenn Koordinaten gefunden wurden, dann Knoten als Drohnenstation hinzufügen
            if x is not None and y is not None:
                stations.append(node_id)
                station_coords[node_id] = (x, y)
    
    # Fall, wenn nur eine Drohnenstation gefunden wurde
    if len(stations) < 2:
        # Gibt keine MST-Kanten, keine Kosten und die 0-1 Stationen zurück
        return [], 0, stations
    
    # Prims Algorithmus

    #Start an zufälliger Station
    rnd = random.randint(0, len(stations)-1)
    start_station = stations[rnd]
    # Startstation schon im MST
    in_mst = set([start_station])
    mst_edges = []
    total_cost = 0
    
    # Priority Queue initialisieren: (distance, from, to)
    pq = []
    
    # Füge alle Kanten vom Startknoten zur PQ hinzu
    x1, y1 = station_coords[start_station]
    # Berechne Distanzen zu allen anderen Stationen
    for other_station in stations:
        if other_station != start_station:
            x2, y2 = station_coords[other_station]
            distance = euclidean_distance(x1, y1, x2, y2)
            heapq.heappush(pq, (distance, start_station, other_station))
    
    # Baue MST auf
    while pq and len(mst_edges) < len(stations) - 1:
        distance, from_station, to_station = heapq.heappop(pq)
        
        # Überspringe wenn Zielknoten schon im MST
        if to_station in in_mst:
            continue
        
        # Füge Kante zum MST hinzu und aktualisiere Kosten
        mst_edges.append((from_station, to_station, distance))
        total_cost += distance
        in_mst.add(to_station)
        
        # Füge alle Kanten vom neuen Knoten zu noch nicht besuchten Knoten hinzu
        x1, y1 = station_coords[to_station]
        for other_station in stations:
            if other_station not in in_mst:
                x2, y2 = station_coords[other_station]
                new_distance = euclidean_distance(x1, y1, x2, y2)
                heapq.heappush(pq, (new_distance, to_station, other_station))
    
    return mst_edges, total_cost, stations


""" 
Eingabe Beispiel:
euclidean_distance(0, 0, 3, 4) 
Ausgabe Beispiel:
5.0

Eingabe Beispiel:
build_station_mst(myDroneNetwork)
Ausgabe Beispiel:
([(HUB, CH1, 5.0), (CH1, RL1, 3.1415) etc.)
"""