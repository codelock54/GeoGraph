import networkx as nx
import numpy as np
from geopy.distance import geodesic

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

class CentroGeneralDelGrafo:
    def __init__(self, grafo):
        self.grafo = grafo

    def calculate_general_median(self):
        min_total_distance = float('inf')
        median_node = None

        for node in self.grafo.nodes:
            total_distance = 0.0
            for neighbor in self.grafo.nodes:
                if node != neighbor:
                    lat1, lon1 = self.grafo.nodes[node]['y'], self.grafo.nodes[node]['x']
                    lat2, lon2 = self.grafo.nodes[neighbor]['y'], self.grafo.nodes[neighbor]['x']
                    distance = haversine(lat1, lon1, lat2, lon2)
                    total_distance += distance

            if total_distance < min_total_distance:
                min_total_distance = total_distance
                median_node = node

        self.median_node = median_node
        self.min_total_distance = min_total_distance

    def calcular(self):
        self.calculate_general_median()
        return self.median_node, self.grafo.nodes[self.median_node]['y'], self.grafo.nodes[self.median_node]['x']

class CentroWeiszfeldDelGrafo:
    def __init__(self, grafo):
        self.grafo = grafo

    def weiszfeld(self, points, epsilon=1e-5):
        points = np.array(points)
        x0 = np.mean(points, axis=0)
        while True:
            num = np.zeros(2)
            den = 0
            for p in points:
                dist = np.linalg.norm(x0 - p)
                if dist == 0:
                    continue
                weight = 1 / dist
                num += p * weight
                den += weight
            x1 = num / den
            if np.linalg.norm(x1 - x0) < epsilon:
                break
            x0 = x1
        return x1

    def calcular(self):
        points = [(data['y'], data['x']) for _, data in self.grafo.nodes(data=True)]
        centroide = self.weiszfeld(points)
        return None, centroide[0], centroide[1]
