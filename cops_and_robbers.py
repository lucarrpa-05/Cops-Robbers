import networkx as nx
from typing import List


class Policia:
    """
    Clase para el policía en el juego. Básicamente persigue al ladrón 
    por el camino más corto.
    """
    
    def __init__(self, initial_position: int):
        """
        Constructor. Le dices dónde empieza el poli.
        
        Args:
            initial_position: Donde arranca el poli, un nodo del grafo
        """
        self.position = initial_position
    
    def move(self, graph: nx.Graph, robber_position: int) -> int:
        """
        Mueve al policía un paso hacia el ladrón. Usa camino más corto.
        
        Args:
            graph: El grafo del juego
            robber_position: Donde está el ladrón ahora mismo
            
        Returns:
            El nuevo nodo donde quedó el poli después de moverse
        """
        # Si ya está en el mismo lugar que el ladrón, no se mueve
        if self.position == robber_position:
            return self.position
            
        # Calcula camino más corto
        try:
            path = nx.shortest_path(graph, self.position, robber_position)
            
            # Solo se mueve un paso
            if len(path) > 1:
                return path[1]  # El siguiente nodo en el camino
            else:
                return self.position  # Se queda quieto si ya está ahí
                
        except nx.NetworkXNoPath:
            # Si no hay camino, que no debería pasar pero por si acaso
            return self.position
    
    def update_position(self, new_position: int) -> None:
        """
        Actualiza la posición. Método trivial pero necesario.
        
        Args:
            new_position: El nuevo nodo donde va a estar
        """
        self.position = new_position


class Ladron:
    """
    Clase para el ladrón. intenta escapar maximizando
    la distancia al policía más cercano
    """
    
    def __init__(self, initial_position: int):
        """
        Constructor. Le dices dónde empieza el ladrón
        
        Args:
            initial_position: Donde arranca el ladrón, un nodo del grafo
        """
        self.position = initial_position
    
    def move(self, graph: nx.Graph, cops_positions: List[int]) -> int:
        """
        Mueve al ladrón intentando alejarse lo más posible de los policías.
        
        Args:
            graph: El grafo donde se juega
            cops_positions: Lista con las posiciones de todos los policías
            
        Returns:
            El nuevo nodo donde quedó el ladrón después de moverse
        """
        # Si no hay policías o el grafo está vacío, no se mueve
        if not cops_positions or graph.number_of_nodes() == 0:
            return self.position
        
        # Si el policía está en el mismo nodo, no puede moverse (está atrapado)
        if self.position in cops_positions:
            return self.position
            
        # Obtiene todos los vecinos (incluyendo quedarse quieto como opción)
        vecinos = list(graph.neighbors(self.position))
        
        # Si no hay vecinos, se queda donde está
        if not vecinos:
            return self.position
            
        # Añade la opción de quedarse quieto
        vecinos.append(self.position)
        
        mejor_posicion = self.position
        max_min_distancia = 0
        
        # Para cada posible movimiento
        for siguiente_pos in vecinos:
            # Si hay un policía en esa posición, no es una opción válida
            if siguiente_pos in cops_positions:
                continue
                
            # Calcula la mínima distancia a cualquier policía desde esta posición
            min_distancia = float('inf')
            
            for pos_policia in cops_positions:
                try:
                    # Distancia al policía
                    distancia = nx.shortest_path_length(graph, siguiente_pos, pos_policia)
                    min_distancia = min(min_distancia, distancia)
                except nx.NetworkXNoPath:
                    # Si no hay camino
                    continue
            
            # Si esta posición es mejor que lo que teníamos
            if min_distancia > max_min_distancia:
                max_min_distancia = min_distancia
                mejor_posicion = siguiente_pos
        
        return mejor_posicion
    
    def update_position(self, new_position: int) -> None:
        """
        Actualiza la posición
        
        Args:
            new_position: El nuevo nodo donde va a estar
        """
        self.position = new_position


# Ejemplo de uso (por si alguien quiere probarlo rápido)
if __name__ == "__main__":
    # Creamos un grafo cualquiera, un árbol random sirve
    grafo = nx.random_tree(10)
    
    # Instanciamos los jugadores en extremos opuestos
    policia = Policia(initial_position=0)
    ladron = Ladron(initial_position=9)
    
    # Simulación del juego
    pasos = 0
    max_pasos = 100  # Para evitar loops infinitos
    
    print(f"Posiciones iniciales - Policía: {policia.position}, Ladrón: {ladron.position}")
    
    while policia.position != ladron.position and pasos < max_pasos:
        pasos += 1
        
        nueva_pos_policia = policia.move(grafo, ladron.position)
        policia.update_position(nueva_pos_policia)
        
        nueva_pos_ladron = ladron.move(grafo, [policia.position])
        ladron.update_position(nueva_pos_ladron)
        
        print(f"Paso {pasos} - Policía: {policia.position}, Ladrón: {ladron.position}")
    
    # Captura o timeout
    if policia.position == ladron.position:
        print(f"El policía atrapó al ladrón en el nodo {policia.position} después de {pasos} pasos.")
    else:
        print(f"La simulación terminó después de {max_pasos} pasos sin captura. Qué aburrido.")
