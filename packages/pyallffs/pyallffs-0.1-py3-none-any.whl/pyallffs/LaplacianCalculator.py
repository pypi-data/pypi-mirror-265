import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import kneighbors_graph
from scipy.sparse.csgraph import laplacian

class LaplacianCalculator:
    def __init__(self, dataframe, drop_labels, target, n_neighbors=5):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target
        self.n_neighbors = n_neighbors

    def calculate_laplacian_feature_score(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        graph = kneighbors_graph(input_data, n_neighbors=self.n_neighbors, mode='distance')
        laplacian_matrix = laplacian(graph, normed=True)

        laplacian_scores = []
        for i in range(input_data.shape[1]):
            feature_vector = input_data.iloc[:, i].values.reshape(-1, 1)
            laplacian_score = np.linalg.norm(laplacian_matrix.dot(feature_vector)) ** 2
            laplacian_scores.append(laplacian_score)

        ranked_features = np.argsort(laplacian_scores)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, laplacian_scores, feature_names)

        return laplacian_scores, ranked_features

    def plot_feature_importance(self, ranked_features, laplacian_scores, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), np.array(laplacian_scores)[ranked_features], color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Laplacian Feature Score')
        plt.title('Laplacian Feature Score for Features')
        plt.tight_layout()
        plt.show()
