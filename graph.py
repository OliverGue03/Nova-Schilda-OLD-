import json


class DroneNetwork:
# Graph für das Drohnenliefernetzwerk mit Adjazenzliste
    
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.all_edges = []
        self.blocked_edges = set()
    
    # Fügt Knoten dem Drohnennetzwerk hinzu
    def add_node(self, node_id, node_data):
        self.nodes[node_id] = node_data
        if node_id not in self.edges:
            self.edges[node_id] = []
    
    # Fügt Kante dem Drohnennetzwerk hinzu
    def add_edge(self, from_id, to_id, edge_data):
        if from_id not in self.edges:
            self.edges[from_id] = []

        self.edges[from_id].append((to_id, edge_data))
        self.all_edges.append((from_id, to_id, edge_data))
        
        # Bidirektionale Kanten
        if edge_data.get('bidirectional', False):
            if to_id not in self.edges:
                self.edges[to_id] = []
            self.edges[to_id].append((from_id, edge_data))
    
    def update_edge_energy(self, from_id, to_id, new_energy):
        if from_id not in self.edges:
            return False
        
        found = False
        for target, data in self.edges[from_id]:
            if target == to_id:
                data['energy_cost'] = new_energy
                found = True
                break
        
        if not found:
            return False
        
        for f, t, d in self.all_edges:
            if f == from_id and t == to_id:
                d['energy_cost'] = new_energy
                break
        
        return True
    
    def update_edge_capacity(self, from_id, to_id, new_capacity):
        if from_id not in self.edges:
            return False
        
        found = False
        for target, data in self.edges[from_id]:
            if target == to_id:
                data['capacity'] = new_capacity
                found = True
                break
        
        if not found:
            return False
        
        for f, t, d in self.all_edges:
            if f == from_id and t == to_id:
                d['capacity'] = new_capacity
                break
        
        return True
    
    def get_neighbors(self, node_id, include_blocked=False):
        neighbors = self.edges.get(node_id, [])
        
        if not include_blocked:
            neighbors = [(target, data) for target, data in neighbors
                        if (node_id, target) not in self.blocked_edges
                        and not data.get('restricted', False)]
        
        return neighbors
    
    def load_from_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for node in data.get('nodes', []):
            node_id = node['id']
            self.add_node(node_id, node)
        
        for edge in data.get('edges', []):
            from_id = edge['from']
            to_id = edge['to']
            edge_data = {k: v for k, v in edge.items() if k not in ['from', 'to']}
            self.add_edge(from_id, to_id, edge_data)
    
    def save_to_json(self, filepath):
        nodes = [self.nodes[node_id] for node_id in self.nodes]
        
        edges = []
        for from_id, to_id, edge_data in self.all_edges:
            edge = {'from': from_id, 'to': to_id}
            edge.update(edge_data)
            edges.append(edge)
        
        data = {'nodes': nodes, 'edges': edges}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def __str__(self):
        return f"DroneNetwork: {len(self.nodes)} nodes, {len(self.all_edges)} edges"
    
    def print_adjacency_list(self):
        # Zeigt vollständige Adjazenzliste
        print("\n" + "="*50)
        print("ADJAZENZLISTE (Alle Knoten und Kanten)")
        print("="*50)
        
        # Knoten sortiert nach Typ
        nodes_by_type = {}
        for node_id, data in self.nodes.items():
            node_type = data.get('type', 'unknown')
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node_id)
        
        print("\nKnoten:")
        for node_type in sorted(nodes_by_type.keys()):
            nodes = sorted(nodes_by_type[node_type])
            print(f"  {node_type}: {', '.join(nodes)}")
        
        print("\nKanten (Adjazenzliste):")
        for node_id in sorted(self.nodes.keys()):
            neighbors = self.get_neighbors(node_id, include_blocked=True)
            if neighbors:
                print(f"\n  {node_id}:")
                for neighbor_id, edge_data in neighbors:
                    energy = edge_data.get('energy_cost', '?')
                    capacity = edge_data.get('capacity', '?')
                    bidir = " <->" if edge_data.get('bidirectional') else " ->"
                    restricted = " [GESPERRT]" if edge_data.get('restricted') else ""
                    blocked = " [BLOCKIERT]" if (node_id, neighbor_id) in self.blocked_edges else ""
                    print(f"    {bidir} {neighbor_id}: Energie={energy}, Kapazität={capacity}{restricted}{blocked}")
            else:
                print(f"\n  {node_id}: (keine Nachbarn)")