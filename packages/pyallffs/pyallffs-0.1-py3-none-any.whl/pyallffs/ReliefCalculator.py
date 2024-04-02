import numpy as np
import matplotlib.pyplot as plt

class ReliefCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_relief(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        n_samples, n_features = input_data.shape
        weights = np.zeros(n_features)

        for i in range(n_samples):
            near_hit_idx = np.argmin(np.linalg.norm(input_data[output_data == output_data.iloc[i]] - input_data.iloc[i], axis=1))
            near_hit = input_data.iloc[near_hit_idx]

            diff_class_idx = np.argmin(np.linalg.norm(input_data[output_data != output_data.iloc[i]] - input_data.iloc[i], axis=1))
            near_miss = input_data.iloc[diff_class_idx]

            weights += -np.square(input_data.iloc[i] - near_hit) + np.square(input_data.iloc[i] - near_miss)

        weights /= n_samples
        ranked_features = np.argsort(weights)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, weights, feature_names)

        return weights, ranked_features

    def plot_feature_importance(self, ranked_features, weights, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), weights[ranked_features], align='center', color='skyblue')
        plt.xticks(range(len(ranked_features)), feature_names[ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Relief Score')
        plt.title('Relief Score for Features')
        plt.tight_layout()
        plt.show()
