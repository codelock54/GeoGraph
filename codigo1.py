import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from math import radians, sin, cos, sqrt, atan2
from shapely.geometry import Polygon

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0 

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


polygon_coords = [
    (-79.01235246943402, -8.089063575510423),
    (-79.0133721279673, -8.090862276022904),
    (-79.00886710610364, -8.093707283966367),
    (-79.00632744070438, -8.089816085888486),
    (-79.00810721994411, -8.089026889639626),
    (-79.0086819095368, -8.08871488074638),
    (-79.01025765335672, -8.088109219336687),
    (-79.0110733244186, -8.089595856518471),
    (-79.01235246943402, -8.089063575510423)
]

polygon = Polygon(polygon_coords)

G = ox.graph_from_polygon(polygon, network_type='drive', simplify=True, retain_all=False)

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.calculate_general_median()

    def calculate_general_median(self):
        min_total_distance = float('inf')
        median_node = None

        for node in self.graph.nodes:
            total_distance = 0.0
            for neighbor in self.graph.nodes:
                if node != neighbor:
                    # Calculate haversine distance between nodes
                    lat1, lon1 = self.graph.nodes[node]['y'], self.graph.nodes[node]['x']
                    lat2, lon2 = self.graph.nodes[neighbor]['y'], self.graph.nodes[neighbor]['x']
                    distance = haversine(lat1, lon1, lat2, lon2)
                    total_distance += distance

            if total_distance < min_total_distance:
                min_total_distance = total_distance
                median_node = node

        self.median_node = median_node
        self.min_total_distance = min_total_distance

    def get_median_node(self):
        return self.median_node

graph = Graph(G)
median_node = graph.get_median_node()

lat, lon = G.nodes[median_node]['y'], G.nodes[median_node]['x']
print(f"Coordenadas del centro hallado: latitud {lat}, longitud {lon}")

def visualize_graph(graph):
    fig, ax = ox.plot_graph(graph.graph, show=False, close=False, node_color='w', node_edgecolor='k')

    x, y = graph.graph.nodes[median_node]['x'], graph.graph.nodes[median_node]['y']
    ax.scatter(x, y, color='red', s=100, label='Centro Absoluto (Mediana General)')
   
    ax.set_title("Red vial en Urb. Chimu", fontsize=15)
    fig.suptitle("Trujillo", fontsize=20)
    ax.legend()

    return fig

class App:
    def __init__(self, root, graph):
        self.root = root
        self.graph = graph

        self.figure = visualize_graph(graph)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root = tk.Tk()
app = App(root, graph)
root.mainloop()
