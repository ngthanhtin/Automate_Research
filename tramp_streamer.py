import sys
import numpy as np
import networkx as nx
from scipy.optimize import minimize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QFormLayout, QTextEdit, QLineEdit, QGridLayout

class GraphOptimizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Graph Optimization')
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.coeff_layout = QFormLayout()
        self.coeff_cost_label = QLabel('Coefficient for Cost:')
        self.coeff_cost_edit = QLineEdit()
        self.coeff_layout.addRow(self.coeff_cost_label, self.coeff_cost_edit)
        self.coeff_profit_label = QLabel('Coefficient for Profit:')
        self.coeff_profit_edit = QLineEdit()
        self.coeff_layout.addRow(self.coeff_profit_label, self.coeff_profit_edit)
        self.layout.addLayout(self.coeff_layout)

        self.label = QLabel('Enter the Number of Nodes:')
        self.layout.addWidget(self.label)

        self.num_nodes_edit = QLineEdit()
        self.layout.addWidget(self.num_nodes_edit)

        self.generate_button = QPushButton('Generate Graph', self)
        self.generate_button.clicked.connect(self.generate_graph)
        self.layout.addWidget(self.generate_button)

        self.cost_profit_label = QLabel('Fill in Cost and Profit Matrix:')
        self.layout.addWidget(self.cost_profit_label)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.optimize_button = QPushButton('Optimize', self)
        self.optimize_button.clicked.connect(self.optimize)
        self.layout.addWidget(self.optimize_button)

        self.result_label = QLabel('Result:')
        self.layout.addWidget(self.result_label)

        self.central_widget.setLayout(self.layout)

    def generate_graph(self):
        num_nodes = int(self.num_nodes_edit.text())
        self.coeff_cost = float(self.coeff_cost_edit.text())
        self.coeff_profit = float(self.coeff_profit_edit.text())

        # Clear the existing grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create input boxes for each cell in the cost-profit matrix
        for source in range(num_nodes):
            for target in range(num_nodes):
                if source != target:
                    cost_profit_edit = QLineEdit()
                    self.grid_layout.addWidget(cost_profit_edit, source, target)

    def parse_graph_data(self):
        num_nodes = int(self.num_nodes_edit.text())
        G = nx.DiGraph()

        for source in range(num_nodes):
            for target in range(num_nodes):
                if source != target:
                    cost_profit_edit = self.grid_layout.itemAtPosition(source, target).widget()
                    input_text = cost_profit_edit.text().strip()
                    if input_text:
                        cost, profit = map(float, input_text.split(','))
                        G.add_edge(source, target, cost=cost, profit=profit)
                    else:
                        cost, profit = np.inf, np.inf
                        G.add_edge(source, target, cost=cost, profit=profit)
        
        return G
    
    def floyd_warshall(self, G):
        # Compute the Floyd-Warshall shortest path distances
        num_nodes = len(G.nodes())
        dist_matrix = np.inf * np.ones((num_nodes, num_nodes))
        
        for i in range(num_nodes):
            dist_matrix[i][i] = 0.

        for u, v, data in G.edges(data=True):
            dist_matrix[u][v] = self.coeff_cost*data['cost'] - self.coeff_profit*data['profit']

        for k in range(num_nodes): # column
            for i in range(num_nodes): # row
                for j in range(num_nodes): # column
                        dist_matrix[i][j] = min(dist_matrix[i][j], dist_matrix[i][k] + dist_matrix[k][j])


        # Check for negative cycles and adjust edge costs if necessary
        for i in range(num_nodes):
            if dist_matrix[i][i] < 0:
                return False, dist_matrix

        return True, dist_matrix

    
    def optimize(self):
        G = self.parse_graph_data()
        dist_matrix = self.floyd_warshall(G)
        print(dist_matrix)
        

def main():
    app = QApplication(sys.argv)
    window = GraphOptimizationApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
