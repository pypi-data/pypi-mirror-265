import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kruskal

class KruskalWallisCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_kruskal_wallis_feature_selection(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        kruskal_results = {}

        for feature in feature_names:
            groups = [input_data[feature][output_data == category] for category in output_data.unique()]
            kruskal_results[feature] = kruskal(*groups).statistic

        ranked_features = sorted(kruskal_results, key=kruskal_results.get, reverse=True)

        if plot_importance:
            self.plot_feature_importance(ranked_features, kruskal_results)

        important_features_indices = [self.dataframe.columns.get_loc(feature) for feature in ranked_features]

        return [kruskal_results[feature] for feature in ranked_features], important_features_indices

    def plot_feature_importance(self, ranked_features, kruskal_results):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), [kruskal_results[feature] for feature in ranked_features], color='skyblue')
        plt.xticks(range(len(ranked_features)), ranked_features, rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Kruskal-Wallis Statistic')
        plt.title('Feature Importance (Kruskal-Wallis Test)')
        plt.tight_layout()
        plt.show()
