from graph import DroneNetwork
import read_testdata
import restrict_path as b2
import network_modification as b3
import check_reachability as f1
import most_efficient_path as f2
import calculate_delivery_capacity as f3
import assess_resilience as f4
import communication_network as f6


def functional_menu(network):
    # Menü für F1-F6
    while True:
        print("\n" + "="*50)
        print("FUNKTIONALE ANFORDERUNGEN")
        print("="*50)
        print("  [1] F1: Erreichbarkeit prüfen")
        print("  [2] F2: Flugrouten berechnen")
        print("  [3] F3: Lieferkapazität")
        print("  [4] F4: Ausfallsicherheit")
        print("  [5] F6: Kommunikationsinfrastruktur")
        print("  [0] Zurück")
        print("="*50)
        
        choice = input("\nAuswahl: ").strip()
        
        if choice == '0':
            break

        elif choice == '1':
            # F1
            hubs = f1.find_all_hubs(network)
            if not hubs:
                print("Keine Hubs gefunden!")
                continue
            
            print(f"\nVerfügbare Hubs: {', '.join(hubs)}")
            
            if len(hubs) == 1:
                hub_id = hubs[0]
                print(f"Verwende Hub: {hub_id}")
            else:
                hub_id = input("Hub auswählen: ").strip()
                if hub_id not in hubs:
                    print("Hub existiert nicht!")
                    continue
            
            print(f"\nPrüfe Erreichbarkeit von {hub_id}1...")
            report = f1.get_reachability_report(network, hub_id)
            
            print(f"\nErgebnis: {'Alle erreichbar' if report['all_reachable'] else 'Nicht alle erreichbar'}")
            print(f"Erreichbare Knoten: {report['total_nodes_reachable']}")
            print(f"Delivery-Punkte: {report['reachable_delivery_points']}/{report['total_delivery_points']}")
            
            if report['unreachable_list']:
                print(f"\nUnerreichbar:")
                for point in report['unreachable_list']:
                    print(f"  - {point}")
        
        elif choice == '2':
            # F2
            print("\nVerfügbare Knoten:")
            nodes_by_type = {}
            for node_id, data in network.nodes.items():
                node_type = data.get('type', 'unknown')
                if node_type not in nodes_by_type:
                    nodes_by_type[node_type] = []
                nodes_by_type[node_type].append(node_id)
            
            for node_type in sorted(nodes_by_type.keys()):
                node_list = ', '.join(nodes_by_type[node_type])
                print(f"  {node_type}: {node_list}")
            
            start = input("\nStartpunkt: ").strip()
            end = input("Zielpunkt: ").strip()
            
            if start not in network.nodes or end not in network.nodes:
                print("Knoten existiert nicht!")
                continue
            
            print(f"\nBerechne Route von {start} nach {end}...")
            route = f2.find_route(network, start, end)
            
            if route['success']:
                print(f"\nRoute gefunden:")
                print(f"  Pfad: {' -> '.join(route['path'])}")
                print(f"  Energie: {route['total_energy']}")
                print(f"  Distanz: {route['total_distance']}")
            else:
                print("Keine Route gefunden!")
        
        elif choice == '3':
            # F3
            hubs = f1.find_all_hubs(network)
            deliveries = []
            for node_id, data in network.nodes.items():
                if data.get('type') == 'delivery':
                    deliveries.append(node_id)
            
            if not hubs:
                print("Keine Hubs!")
                continue
            
            if not deliveries:
                print("Keine Delivery-Punkte!")
                continue
            
            # Hub auswählen
            print(f"\nVerfügbare Hubs: {', '.join(hubs)}")
            if len(hubs) == 1:
                hub_id = hubs[0]
                print(f"Verwende Hub: {hub_id}")
            else:
                hub_id = input("Hub auswählen: ").strip()
                if hub_id not in hubs:
                    print("Hub existiert nicht!")
                    continue
            
            # Urban Area definieren
            print(f"\nVerfügbare Delivery-Punkte: {', '.join(deliveries)}")
            print("\nUrban Area definieren (Stadtgebiet mit mehreren Delivery-Punkten):")
            print("Geben Sie Delivery-Punkt IDs ein (kommagetrennt)")
            area_input = input("Urban Area: ").strip()
            
            delivery_area = []
            for point_id in area_input.split(','):
                point_id = point_id.strip()
                if point_id in deliveries:
                    delivery_area.append(point_id)
                else:
                    print(f"Warnung: {point_id} ist kein gültiger Delivery-Punkt")
            
            if not delivery_area:
                print("Keine gültige Urban Area definiert!")
                continue
            
            print(f"\nUrban Area: {', '.join(delivery_area)}")
            print(f"Berechne Kapazität von {hub_id} zu Urban Area...")
            print("(capacity = max. Drohnen/Stunde pro Korridor)")
            capacity = f3.calculate_delivery_capacity(network, hub_id, delivery_area)
            
            print(f"\nErgebnis:")
            print(f"  Maximale Kapazität: {capacity['max_capacity']} Drohnen/h")
            print(f"  Verwendete Korridore: {len(capacity['used_edges'])}")
        
        elif choice == '4':
            # F4 - Ausfallsicherheit
            print("\nAnalysiere Ausfallsicherheit...")
            resilience = f4.analyze_network_resilience(network)
            
            # Engpässe (Bottlenecks)
            print("\n" + "="*50)
            print("1. ENGPÄSSE (Bottlenecks)")
            print("="*50)
            print("Kanten mit geringer Kapazität, die Flow begrenzen:")
            
            if resilience.get('bottlenecks'):
                for from_id, to_id, capacity in resilience['bottlenecks']:
                    print(f"  {from_id} -> {to_id}: Kapazität={capacity}")
            else:
                print("  Keine Engpässe gefunden.")
            
            # Trenn-Set (Bridges)
            print("\n" + "="*50)
            print("2. BRIDGES (Kritische Kanten)")
            print("="*50)
            print("Kanten deren Entfernung Netzwerk in Teile trennt:")
            
            if resilience['bridges']:
                print(f"  Gefunden: {len(resilience['bridges'])} kritische Kante(n)")
                for u, v in resilience['bridges']:
                    print(f"    {u} <-> {v}")
            else:
                print("  Keine Bridges gefunden.")
        
        
        elif choice == '5':
            # F6 - Kommunikationsinfrastruktur
            print("\nBerechne Kommunikationsnetz für Drohnenstationen...")
            
            mst_edges, total_cost, stations = f6.build_station_mst(network)
            
            if len(stations) < 2:
                print("Nicht genug Stationen!")
                continue
            
            print(f"\nDrohnenstationen: {len(stations)}")
            print(f"  {', '.join(stations)}")
            
            print(f"\nMST Ergebnis:")
            print(f"  Verbindungen: {len(mst_edges)}")
            print(f"  Gesamtkosten: {total_cost:.1f} Tausend Euro")
            print(f"\nRichtfunknetzwerk eingerichtet")
            if mst_edges:
                print(f"\nRichtfunkverbindungen:")
                for u, v, cost in sorted(mst_edges, key=lambda x: x[2]):
                    print(f"  {u} <-> {v}: {cost:.1f}")
        
        else:
            print("Ungültige Auswahl!")


def basic_menu(network):
    # Menü für B2 und B3
    while True:
        print("\n" + "="*50)
        print("BASISFUNKTIONEN")
        print("="*50)
        print("  [1] Korridor sperren (temporär)")
        print("  [2] Korridor sperren (permanent)")
        print("  [3] Korridor entsperren")
        print("  [4] Hub hinzufügen")
        print("  [5] Ladestation hinzufügen")
        print("  [6] Flugkorridor hinzufügen")
        print("  [7] Energie ändern")
        print("  [8] Kapazität ändern")
        print("  [9] Netzwerk speichern")
        print("  [0] Zurück")
        print("="*50)
        
        choice = input("\nAuswahl: ").strip()
        
        if choice == '0':
            break

        elif choice == '1':
            from_id = input("Von: ").strip()
            to_id = input("Zu: ").strip()
            if b2.block_corridor(network, from_id, to_id, temporary=True):
                print(f"Gesperrt: {from_id} -> {to_id}")
            else:
                print("Korridor existiert nicht!")

        elif choice == '2':
            from_id = input("Von: ").strip()
            to_id = input("Zu: ").strip()
            if b2.block_corridor(network, from_id, to_id, temporary=False):
                print(f"Permanent gesperrt: {from_id} -> {to_id}")
            else:
                print("Korridor existiert nicht!")

        elif choice == '3':
            from_id = input("Von: ").strip()
            to_id = input("Zu: ").strip()
            if b2.unblock_corridor(network, from_id, to_id):
                print(f"Entsperrt: {from_id} -> {to_id}")
            else:
                print("War nicht gesperrt!")

        elif choice == '4':
            hub_id = input("Hub-ID: ").strip()
            x = float(input("X: ").strip())
            y = float(input("Y: ").strip())
            name = input("Name (optional): ").strip()
            if b3.add_hub(network, hub_id, x, y, name if name else None):
                print(f"Hub {hub_id} hinzugefügt")
            else:
                print("ID existiert bereits!")

        elif choice == '5':
            station_id = input("ID: ").strip()
            x = float(input("X: ").strip())
            y = float(input("Y: ").strip())
            if b3.add_charging_station(network, station_id, x, y):
                print(f"Ladestation {station_id} hinzugefügt")
            else:
                print("ID existiert bereits!")

        elif choice == '6':
            from_id = input("Von: ").strip()
            to_id = input("Zu: ").strip()
            energy = float(input("Energie: ").strip())
            capacity = int(input("Kapazität: ").strip())
            if b3.add_flight_corridor(network, from_id, to_id, energy, capacity):
                print(f"Korridor {from_id} -> {to_id} hinzugefügt")
            else:
                print("Knoten existieren nicht!")

        elif choice == '7':
            from_id = input("Von: ").strip()
            to_id = input("Zu: ").strip()
            new_energy = float(input("Neue Energie: ").strip())
            if b3.modify_corridor_energy(network, from_id, to_id, new_energy):
                print("Energie geändert")
            else:
                print("Korridor existiert nicht!")

        elif choice == '8':
            from_id = input("Von: ").strip()
            to_id = input("Zu: ").strip()
            new_capacity = int(input("Neue Kapazität: ").strip())
            if b3.modify_corridor_capacity(network, from_id, to_id, new_capacity):
                print("Kapazität geändert")
            else:
                print("Korridor existiert nicht!")

        elif choice == '9':
            filename = input("Dateiname: ").strip()
            network.save_to_json(filename)
            print(f"Gespeichert: {filename}")
        else:
            print("Ungültige Auswahl!")


def main():
    # Hauptfunktion
    print("="*50)
    print(" Drohnenliefersystem - Nova Schilda")
    print("="*50)
    
    network = None
    
    while True:
        print("\n" + "="*50)
        print("HAUPTMENÜ")
        print("="*50)
        print("  [1] B1: Netzwerk laden")
        print("  [2] Adjazenzliste anzeigen")
        print("  [3] Basisfunktionen (B2, B3)")
        print("  [4] Funktionale Anforderungen (F1-F4, F6)")
        print("  [0] Beenden")
        print("="*50)
        
        choice = input("\nAuswahl: ").strip()
        
        if choice == '0':
            print("\nProgramm beendet.")
            break

        elif choice == '1':
            filepath = read_testdata.select_json_file()
            if filepath:
                try:
                    network = DroneNetwork()
                    network.load_from_json(filepath)
                    print(f"\nNetzwerk geladen: {filepath}")
                    print(f"{network}")
                except Exception as e:
                    print(f"\nFehler: {e}")
                    network = None

        elif choice == '2':
            if network:
                network.print_adjacency_list()
            else:
                print("\nKein Netzwerk geladen!")

        elif choice == '3':
            if network:
                basic_menu(network)
            else:
                print("\nKein Netzwerk geladen!")

        elif choice == '4':
            if network:
                functional_menu(network)
            else:
                print("\nKein Netzwerk geladen!")
                
        else:
            print("\nUngültige Auswahl!")


if __name__ == "__main__":
    main()