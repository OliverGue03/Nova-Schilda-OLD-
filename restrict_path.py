# B2: Sperrzonen einrichten

def block_corridor(network, from_id, to_id, temporary=True):
    # Überprüfen, ob die Kante existiert
    if from_id not in network.edges:
        return False
    
    # Kante finden und sperren
    edge_exists = False
    for target, data in network.edges[from_id]:
        if target == to_id:
            edge_exists = True
            if not temporary:
                data['restricted'] = True
                for f, t, d in network.all_edges:
                    if f == from_id and t == to_id:
                        d['restricted'] = True
                        break
            break
    
    # Wenn die Kante nicht existiert, Rückgabe False
    if not edge_exists:
        return False
    
    # Bei temporärer Sperrung Kante zur Liste der blockierten Kanten hinzufügen
    if temporary:
        network.blocked_edges.add((from_id, to_id))
    
    return True


def unblock_corridor(network, from_id, to_id):
    # Hebt temporäre Sperrung auf
    if (from_id, to_id) in network.blocked_edges:
        network.blocked_edges.remove((from_id, to_id))
        return True
    # Bei permanent gesperrten Kanten wird nichts gemacht
    return False


"""
Beispiel Eingabe:
block_corridor(myDroneNetwork, 'A', 'B', temporary=False)
Beispiel Ausgabe:
True

Beispiel Eingabe:
unblock_corridor(myDroneNetwork, 'A', 'B')
Beispiel Ausgabe:
False
"""
