import osmnx as ox
import networkx as nx
import numpy as np
from shapely.geometry import Polygon, Point
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Función para calcular el punto de Fermat-Weber usando el algoritmo de Weiszfeld
def weiszfeld(points, epsilon=1e-5):
    points = np.array(points)
    x0 = np.mean(points, axis=0)  # Starting point (centroid)
    while True:
        num = np.zeros(2)
        den = 0
        for p in points:
            dist = np.linalg.norm(x0 - p)
            if dist == 0:  # Avoid division by zero
                continue
            weight = 1 / dist
            num += p * weight
            den += weight
        x1 = num / den
        if np.linalg.norm(x1 - x0) < epsilon:
            break
        x0 = x1
    return x1

# Coordenadas del polígono
coords = [
    [-79.00643737102791, -8.099180191401771],
    [-79.0075183067919, -8.101610325800735],
    [-79.0092973469038, -8.100696240270452],
    [-79.01112142600574, -8.10283653483603],
    [-79.01064851660878, -8.103527669192019],
    [-79.01024316569729, -8.104441748291293],
    [-79.01017560721226, -8.105155174437186],
    [-79.01118898449079, -8.107072500937463],
    [-79.00380259010299, -8.105868599318782],
    [-79.00391518757849, -8.105222058074233],
    [-79.00294684928998, -8.103393901345257],
    [-79.00238386191299, -8.102992597536556],
    [-79.00414038252944, -8.100763124648537],
    [-79.00479344788694, -8.100205754496216],
    [-79.00643737102791, -8.099180191401771]
]

# Crear un polígono
polygon = Polygon(coords)

# Descargar el grafo vial usando osmnx
G = ox.graph_from_polygon(polygon, network_type='drive')

# Encontrar los nodos más cercanos a las coordenadas del polígono
nodes = [ox.distance.nearest_nodes(G, coord[0], coord[1]) for coord in coords]

# Obtener las coordenadas de los nodos
node_coords = [[G.nodes[node]['y'], G.nodes[node]['x']] for node in nodes]

# Encontrar el punto de Fermat-Weber
fw_point = weiszfeld(node_coords)

# Convertir el punto de Fermat-Weber a una tupla para geopy
fw_point_tuple = (fw_point[0], fw_point[1])

# Calcular la distancia total desde el punto de Fermat-Weber a todos los puntos usando la fórmula de Haversine
total_distance = sum(geodesic(fw_point_tuple, (coord[1], coord[0])).meters for coord in coords)

print(f"Punto de Fermat-Weber: {fw_point_tuple}")
print(f"Distancia total desde el punto de Fermat-Weber a todos los puntos: {total_distance:.2f} metros")

# Visualizar el Polígono, el Grafo y el Punto de Fermat-Weber
fig, ax = ox.plot_graph(G, show=False, close=False)
x, y = polygon.exterior.xy
ax.plot(x, y, 'o-', color='blue', label='Polígono')
ax.plot(fw_point[1], fw_point[0], 'x', color='red', label='Punto de Fermat-Weber')
plt.title('Polígono, Grafo Vial y Punto de Fermat-Weber')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.legend()
plt.grid(True)
plt.show()
