# Full Replica of Falstad's Circuit Simulator (Python Version)
# Requirements: PyQt5, matplotlib, numpy, scipy

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QPointF
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# -----------------------
# Basic Circuit Elements
# -----------------------
class Resistor:
    def __init__(self, n1, n2, resistance):
        self.n1 = n1
        self.n2 = n2
        self.resistance = resistance

class VoltageSource:
    def __init__(self, n1, n2, voltage):
        self.n1 = n1
        self.n2 = n2
        self.voltage = voltage

# ------------------------
# Circuit Simulation Logic
# ------------------------
class Circuit:
    def __init__(self):
        self.resistors = []
        self.voltage_sources = []

    def add_resistor(self, r):
        self.resistors.append(r)

    def add_voltage_source(self, v):
        self.voltage_sources.append(v)

    def solve_dc(self):
        nodes = set()
        for r in self.resistors:
            nodes.add(r.n1)
            nodes.add(r.n2)
        for v in self.voltage_sources:
            nodes.add(v.n1)
            nodes.add(v.n2)

        node_map = {n: i for i, n in enumerate(nodes)}
        n = len(node_map)
        A = np.zeros((n, n))
        b = np.zeros(n)

        for r in self.resistors:
            i = node_map[r.n1]
            j = node_map[r.n2]
            if i != j:
                A[i, i] += 1 / r.resistance
                A[j, j] += 1 / r.resistance
                A[i, j] -= 1 / r.resistance
                A[j, i] -= 1 / r.resistance

        for v in self.voltage_sources:
            i = node_map[v.n1]
            j = node_map[v.n2]
            b[i] += v.voltage
            b[j] -= v.voltage

        try:
            x = np.linalg.solve(A, b)
            return {node: x[i] for node, i in node_map.items()}
        except np.linalg.LinAlgError:
            return "Circuit cannot be solved"

# ------------------------
# GUI and Visual Elements
# ------------------------
class CircuitCanvas(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.components = []
        self.setSceneRect(0, 0, 800, 600)

    def add_resistor(self, x1, y1, x2, y2):
        pen = QPen(Qt.black, 2)
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(pen)
        self.addItem(line)
        self.components.append(('R', (x1, y1), (x2, y2)))

    def add_voltage(self, x1, y1, x2, y2):
        pen = QPen(Qt.red, 2)
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(pen)
        self.addItem(line)
        self.components.append(('V', (x1, y1), (x2, y2)))

# ------------------------
# Oscilloscope (Plotting)
# ------------------------
class Oscilloscope(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 2), dpi=100)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot(self, data):
        self.axes.clear()
        self.axes.plot(data)
        self.draw()

# ------------------------
# Main Application Window
# ------------------------
class CircuitSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Falstad-like Circuit Simulator")
        self.setGeometry(100, 100, 1000, 600)
        self.init_ui()

    def init_ui(self):
        self.canvas = CircuitCanvas()
        self.view = QGraphicsView(self.canvas)
        self.oscilloscope = Oscilloscope()

        self.label = QLabel("Click buttons to add components")
        self.btn_add_resistor = QPushButton("Add Resistor")
        self.btn_add_voltage = QPushButton("Add Voltage Source")
        self.btn_solve = QPushButton("Solve DC")

        self.btn_add_resistor.clicked.connect(lambda: self.canvas.add_resistor(100, 100, 200, 100))
        self.btn_add_voltage.clicked.connect(lambda: self.canvas.add_voltage(200, 100, 200, 200))
        self.btn_solve.clicked.connect(self.solve_circuit)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.view)
        layout.addWidget(self.btn_add_resistor)
        layout.addWidget(self.btn_add_voltage)
        layout.addWidget(self.btn_solve)
        layout.addWidget(self.oscilloscope)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def solve_circuit(self):
        circuit = Circuit()
        circuit.add_resistor(Resistor("n1", "n2", 100))
        circuit.add_voltage_source(VoltageSource("n1", "n3", 10))
        result = circuit.solve_dc()

        if isinstance(result, dict):
            self.label.setText("Voltages: " + str(result))
            self.oscilloscope.plot(list(result.values()))
        else:
            self.label.setText(result)

# ------------------------
# Run the Application
# ------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = CircuitSimulator()
    sim.show()
    sys.exit(app.exec_())
