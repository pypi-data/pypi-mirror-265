import numpy as np
import matplotlib.pyplot as plt

class EuclideanDistanceCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_euclidean_distance_feature_selection(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        euclidean_distances = []
        for feature in input_data.columns:
            euclidean_distance = np.linalg.norm(input_data[feature] - output_data)
            euclidean_distances.append(euclidean_distance)

        ranked_features = np.argsort(euclidean_distances)[::-1]
        sorted_distances = np.sort(euclidean_distances)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, sorted_distances, feature_names)

        return sorted_distances, ranked_features

    def plot_feature_importance(self, ranked_features, sorted_distances, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), sorted_distances, color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Euclidean Distance')
        plt.ylabel('Features')
        plt.title('Feature Importance (Euclidean Distance)')
        plt.tight_layout()
        plt.show()
