import sys
from math import radians, sin, cos, sqrt, atan2
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QHBoxLayout
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
from shapely.geometry import Polygon
import numpy as np
import Creargrafo as gu
from metodos import CentroGeneralDelGrafo, CentroWeiszfeldDelGrafo
from Poligonos import Polygons

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lat2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Análisis de Grafo con PyQt6")

        # Create a custom title bar with a centered title
        self.title_bar = QWidget()
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel("Análisis de Grafo con PyQt6")
        self.title_label.setFont(QFont('Arial', 16))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_layout.addWidget(QLabel())
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addWidget(QLabel())

        self.title_bar.setLayout(self.title_layout)
        self.title_layout.setStretch(0, 1)
        self.title_layout.setStretch(1, 10)
        self.title_layout.setStretch(2, 1)

        layout = QVBoxLayout()
        layout.addWidget(self.title_bar)

        self.canvas = FigureCanvas(plt.Figure(figsize=(10, 8)))

        layout_content = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.canvas)

        self.combo_poligono = QComboBox()
        self.combo_poligono.addItems(["TV20", "TV50", "TV51"])
        left_layout.addWidget(self.combo_poligono)

        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Centro General del Grafo", "Centro Weiszfeld del Grafo"])
        self.combo_metodo.setEnabled(False)  # Initially disabled
        left_layout.addWidget(self.combo_metodo)

        self.combo_display = QComboBox()
        self.combo_display.addItems(["Solo Nodos", "Solo Polígono", "Nodos con Distancias", "Centro"])
        self.combo_display.currentIndexChanged.connect(self.habilitar_calculo)  # Connect the method to the change signal
        left_layout.addWidget(self.combo_display)

        self.boton_calcular = QPushButton("Calcular Centro")
        self.boton_calcular.setEnabled(False)  # Initially disabled
        self.boton_calcular.clicked.connect(self.calcular_centro)
        left_layout.addWidget(self.boton_calcular)

        self.etiqueta_resultado = QLabel("Resultado:")
        left_layout.addWidget(self.etiqueta_resultado)

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://www.google.com/maps"))

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.web_view)

        self.boton_maps = QPushButton("Buscar en Google Maps")
        self.boton_maps.clicked.connect(self.abrir_en_google_maps)
        right_layout.addWidget(self.boton_maps)

        layout_content.addLayout(left_layout)
        layout_content.addLayout(right_layout)

        layout_content.setStretch(0, 4)  # Increase the stretch factor of the left layout
        layout_content.setStretch(1, 4)  # Decrease the stretch factor of the right layout

        layout.addLayout(layout_content)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.lat_central = None
        self.lon_central = None

    def obtener_poligono(self):
        poligono_nombre = self.combo_poligono.currentText()
        if poligono_nombre == "TV20":
            return Polygons.TV20()
        elif poligono_nombre == "TV50":
            return Polygons.TV50()
        elif poligono_nombre == "TV51":
            return Polygons.TV51()

    def habilitar_calculo(self):
        display_option = self.combo_display.currentText()
        if display_option == "Centro":
            self.combo_metodo.setEnabled(True)
            self.boton_calcular.setEnabled(True)
        else:
            self.combo_metodo.setEnabled(False)
            self.boton_calcular.setEnabled(False)

    def calcular_centro(self):
        poligono = self.obtener_poligono()

        G = gu.crear_grafo_desde_poligono(poligono)

        metodo = self.combo_metodo.currentText()
        if metodo == "Centro General del Grafo":
            centro_calculador = CentroGeneralDelGrafo(G)
            metodo_texto = "Centro General del Grafo"
            nodo_central, self.lat_central, self.lon_central = centro_calculador.calcular()
            x, y = G.nodes[nodo_central]['x'], G.nodes[nodo_central]['y']
        else:
            centro_calculador = CentroWeiszfeldDelGrafo(G)
            metodo_texto = "Centro Weiszfeld del Grafo"
            nodo_central, self.lat_central, self.lon_central = centro_calculador.calcular()
            x, y = self.lon_central, self.lat_central

        self.etiqueta_resultado.setText(f'Resultado: Nodo {nodo_central}, Latitud {self.lat_central}, Longitud {self.lon_central}')

        display_option = self.combo_display.currentText()

        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)

        ax.set_facecolor('black')
        self.canvas.figure.patch.set_facecolor('black')

        if display_option == "Solo Nodos":
            fig, ax = ox.plot_graph(G, show=False, close=False, node_color='white', node_edgecolor='black', bgcolor='black', edge_color='gray', ax=ax)
            ax.set_title("Nodos")
        elif display_option == "Solo Polígono":
            x_poly, y_poly = zip(*poligono)
            ax.plot(x_poly, y_poly, 'o-', color='blue', label='Polígono')
            ax.set_title("Polígono")
        elif display_option == "Nodos con Distancias":
            fig, ax = ox.plot_graph(G, show=False, close=False, node_color='white', node_edgecolor='black', bgcolor='black', edge_color='gray', ax=ax)
            for u, v, data in G.edges(data=True):
                distance_label = f"{data['length'] / 1000:.2f} km" if 'length' in data else f"{haversine(G.nodes[u]['y'], G.nodes[u]['x'], G.nodes[v]['y'], G.nodes[v]['x']):.2f} km"
                x = (G.nodes[u]['x'] + G.nodes[v]['x']) / 2
                y = (G.nodes[u]['y'] + G.nodes[v]['y']) / 2
                offset_x = 0.0005  # Ajusta este valor según sea necesario
                offset_y = 0.0005  # Ajusta este valor según sea necesario
                ax.text(x + offset_x, y + offset_y, distance_label, fontsize=8, ha='center', color='red')
            ax.set_title("Nodos con Distancias")
        else:  # "Centro"
            fig, ax = ox.plot_graph(G, show=False, close=False, edge_color='gray', node_color='white', node_edgecolor='black', bgcolor='black', ax=ax)
            ax.scatter(x, y, color='red', s=100, zorder=5, label=metodo_texto)
            x_poly, y_poly = zip(*poligono)
            ax.plot(x_poly, y_poly, 'o-', color='blue', label='Polígono')
            ax.set_title("Centro")

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), frameon=True, framealpha=0.9, facecolor='lightgray', edgecolor='black')
        self.canvas.draw()

    def abrir_en_google_maps(self):
        if self.lat_central is not None and self.lon_central is not None:
            url = f"https://maps.googleapis.com/maps/api/staticmap?center={self.lat_central},{self.lon_central}&zoom=15&size=600x400&markers=color:red%7C{self.lat_central},{self.lon_central}&key=YOUR_API_KEY"
            self.web_view.setUrl(QUrl(url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
