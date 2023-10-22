## graph_generator.py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List

class GraphGenerator:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def generate_graph(self, x_data: List[int], y_data: List[int], z_data: List[int]):
        self.ax.scatter(x_data, y_data, z_data, c='r', marker='o')

        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')

        return plt.show()

    def compare_text(self, text1: str, text2: str) -> float:
        # TODO: Implement the text comparison logic using OpenAI's Ada model
        raise NotImplementedError("The method compare_text is not implemented.")
