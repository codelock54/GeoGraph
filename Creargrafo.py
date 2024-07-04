import osmnx as ox
from shapely.geometry import Polygon

def crear_grafo_desde_poligono(coordenadas_poligono):
    poligono = Polygon(coordenadas_poligono)
    G = ox.graph_from_polygon(poligono, network_type='drive', simplify=False, truncate_by_edge=True)
    return G
