import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as ss

class CramersVCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_cramers_v_feature_selection(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        cramer_vs = []
        for feature in input_data.columns:
            confusion_matrix = pd.crosstab(input_data[feature], output_data)
            chi2, _, _, _ = ss.chi2_contingency(confusion_matrix)
            n = confusion_matrix.sum().sum()
            min_dim = min(confusion_matrix.shape) - 1
            cramer_v = np.sqrt(chi2 / (n * min_dim))
            cramer_vs.append(cramer_v)

        ranked_features = np.argsort(cramer_vs)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, cramer_vs, feature_names)

        return cramer_vs, ranked_features

    def plot_feature_importance(self, ranked_features, cramer_vs, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), np.array(cramer_vs)[ranked_features], color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel("Cramer's V Value")
        plt.title("Feature Importance (Cramer's V)")
        plt.tight_layout()
        plt.show()
