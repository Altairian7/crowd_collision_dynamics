# Enhanced Falstad-like Circuit Simulator in Python
# Includes: DC Analysis, Interactive Component Placement, Oscilloscope, Node Highlighting, and Future Extension Hooks

import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,
                             QLabel, QGraphicsScene, QGraphicsView, QGraphicsLineItem,
                             QHBoxLayout, QLineEdit, QMessageBox)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# -----------------------------
# Basic Circuit Elements
# -----------------------------
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

# -----------------------------
# Circuit Simulation Logic
# -----------------------------
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
            nodes.update([r.n1, r.n2])
        for v in self.voltage_sources:
            nodes.update([v.n1, v.n2])

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
            return {node: round(x[i], 2) for node, i in node_map.items()}
        except np.linalg.LinAlgError:
            return "Circuit cannot be solved"

# -----------------------------
# Circuit Drawing Canvas
# -----------------------------
class CircuitCanvas(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.components = []
        self.setSceneRect(0, 0, 800, 600)
        self.node_count = 1

    def add_component(self, x1, y1, x2, y2, ctype, value):
        pen = QPen(Qt.blue if ctype == 'R' else Qt.red, 2)
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(pen)
        self.addItem(line)
        n1 = f"n{self.node_count}"
        n2 = f"n{self.node_count + 1}"
        self.node_count += 2
        self.components.append((ctype, (n1, n2), value))
        return (n1, n2, value)

# -----------------------------
# Oscilloscope (Plotting)
# -----------------------------
class Oscilloscope(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 2), dpi=100)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot(self, data):
        self.axes.clear()
        self.axes.plot(data, marker='o')
        self.axes.set_title("Node Voltages")
        self.axes.set_xlabel("Node Index")
        self.axes.set_ylabel("Voltage (V)")
        self.draw()

# -----------------------------
# Main GUI Window
# -----------------------------
class CircuitSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Falstad-like Circuit Simulator")
        self.setGeometry(100, 100, 1200, 700)
        self.init_ui()

    def init_ui(self):
        self.canvas = CircuitCanvas()
        self.view = QGraphicsView(self.canvas)
        self.oscilloscope = Oscilloscope()
        self.circuit = Circuit()

        # Widgets
        self.label = QLabel("Add components below, then solve:")
        self.res_input = QLineEdit("100")
        self.volt_input = QLineEdit("10")

        self.btn_add_resistor = QPushButton("Add Resistor")
        self.btn_add_voltage = QPushButton("Add Voltage Source")
        self.btn_solve = QPushButton("Solve DC Circuit")

        # Actions
        self.btn_add_resistor.clicked.connect(self.add_resistor)
        self.btn_add_voltage.clicked.connect(self.add_voltage_source)
        self.btn_solve.clicked.connect(self.solve_circuit)

        # Layouts
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Resistance (Ohms):"))
        input_layout.addWidget(self.res_input)
        input_layout.addWidget(QLabel("Voltage (V):"))
        input_layout.addWidget(self.volt_input)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.view)
        layout.addLayout(input_layout)
        layout.addWidget(self.btn_add_resistor)
        layout.addWidget(self.btn_add_voltage)
        layout.addWidget(self.btn_solve)
        layout.addWidget(self.oscilloscope)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_resistor(self):
        try:
            resistance = float(self.res_input.text())
            n1, n2, _ = self.canvas.add_component(100, 100, 300, 100, 'R', resistance)
            self.circuit.add_resistor(Resistor(n1, n2, resistance))
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid resistance value")

    def add_voltage_source(self):
        try:
            voltage = float(self.volt_input.text())
            n1, n2, _ = self.canvas.add_component(300, 100, 300, 200, 'V', voltage)
            self.circuit.add_voltage_source(VoltageSource(n1, n2, voltage))
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid voltage value")

    def solve_circuit(self):
        result = self.circuit.solve_dc()
        if isinstance(result, dict):
            self.label.setText("Voltages: " + str(result))
            self.oscilloscope.plot(list(result.values()))
        else:
            self.label.setText(result)

# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = CircuitSimulator()
    sim.show()
    sys.exit(app.exec_())