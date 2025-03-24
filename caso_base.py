import networkx as nx
import matplotlib.pyplot as plt
import os
from cops_and_robbers import Policia, Ladron

# Asegurar que la carpeta de imágenes existe
carpeta_imagenes = "imagenes"
if not os.path.exists(carpeta_imagenes):
    os.makedirs(carpeta_imagenes)

# Función para visualizar el grafo
def visualizar_grafo(grafo, pos_policia, pos_ladron, paso, nombre_prueba):
    plt.figure(figsize=(10, 6))
    
    # Posiciones para dibujar el grafo
    pos = nx.spring_layout(grafo, seed=42)
    
    # Dibujar el grafo
    nx.draw(grafo, pos, with_labels=True, node_color='lightgray', 
            node_size=500, font_size=15, width=2, edge_color='gray')
    
    # Dibujar el policía (rojo)
    nx.draw_networkx_nodes(grafo, pos, nodelist=[pos_policia], 
                          node_color='red', node_size=700)
    
    # Dibujar el ladrón (azul)
    nx.draw_networkx_nodes(grafo, pos, nodelist=[pos_ladron], 
                          node_color='blue', node_size=700)
    
    plt.title(f"{nombre_prueba} - Paso {paso}: Policía (rojo) en {pos_policia}, Ladrón (azul) en {pos_ladron}")
    plt.savefig(os.path.join(carpeta_imagenes, f"{nombre_prueba}_paso_{paso}.png"))
    plt.close()

# Función para ejecutar una simulación completa
def ejecutar_simulacion(grafo, pos_inicial_policia, pos_inicial_ladron, max_pasos, nombre_prueba):
    # Instanciar jugadores
    policia = Policia(initial_position=pos_inicial_policia)
    ladron = Ladron(initial_position=pos_inicial_ladron)
    
    print(f"\n--- Iniciando simulación: {nombre_prueba} ---")
    print(f"Posiciones iniciales - Policía: {policia.position}, Ladrón: {ladron.position}")
    
    # Visualizar estado inicial
    visualizar_grafo(grafo, policia.position, ladron.position, 0, nombre_prueba)
    
    # Ejecutar la simulación
    pasos = 0
    
    while policia.position != ladron.position and pasos < max_pasos:
        pasos += 1
        
        # Mover policía
        nueva_pos_policia = policia.move(grafo, ladron.position)
        policia.update_position(nueva_pos_policia)
        
        # Mover ladrón
        nueva_pos_ladron = ladron.move(grafo, [policia.position])
        ladron.update_position(nueva_pos_ladron)
        
        print(f"Paso {pasos} - Policía: {policia.position}, Ladrón: {ladron.position}")
        
        # Visualizar este paso
        visualizar_grafo(grafo, policia.position, ladron.position, pasos, nombre_prueba)
    
    # Resultado final
    if policia.position == ladron.position:
        print(f"El policía atrapó al ladrón en el nodo {policia.position} después de {pasos} pasos.")
        return True, pasos
    else:
        print(f"La simulación terminó después de {max_pasos} pasos sin captura.")
        return False, max_pasos

# CASO 1: Grafo camino (path graph)
# 0 -- 1 -- 2 -- 3 -- 4
grafo_camino = nx.path_graph(5)
ejecutar_simulacion(grafo_camino, 0, 4, 10, "grafo_camino")

# CASO 2: Grafo ciclo (cycle graph)
# 0 -- 1 -- 2
# |         |
# 5 -- 4 -- 3
grafo_ciclo = nx.cycle_graph(6)
ejecutar_simulacion(grafo_ciclo, 0, 3, 10, "grafo_ciclo")

# CASO 3: Grafo árbol simple (resultado conocido)
# Creamos un árbol simple donde sabemos que el policía debe atrapar al ladrón
#       0
#      / \
#     1   2
#    /     \
#   3       4
grafo_arbol = nx.Graph()
grafo_arbol.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 4)])

print("\n--- CASO DE PRUEBA CON RESULTADO CONOCIDO ---")
print("En un árbol, un solo policía siempre puede atrapar a un ladrón si ambos juegan óptimamente.")
print("El policía debe atrapar al ladrón en este caso.")

capturado, pasos = ejecutar_simulacion(grafo_arbol, 0, 4, 10, "grafo_arbol")

if capturado:
    print(" PRUEBA EXITOSA: El policía atrapó al ladrón como se esperaba en un árbol.")
else:
    print(" ERROR: El policía debería haber atrapado al ladrón en un árbol.")

# CASO 4: Grafo completo (resultado conocido)
# En un grafo completo, el policía debe atrapar al ladrón en el primer paso
grafo_completo = nx.complete_graph(5)

print("\n--- CASO DE PRUEBA CON RESULTADO CONOCIDO ---")
print("En un grafo completo, un policía debe atrapar al ladrón en el primer paso.")

capturado, pasos = ejecutar_simulacion(grafo_completo, 0, 4, 5, "grafo_completo")

if capturado and pasos == 1:
    print(" PRUEBA EXITOSA: El policía atrapó al ladrón en el primer paso como se esperaba.")
else:
    print(f" ERROR: El policía debería haber atrapado al ladrón en el primer paso, pero tomó {pasos} pasos.")
