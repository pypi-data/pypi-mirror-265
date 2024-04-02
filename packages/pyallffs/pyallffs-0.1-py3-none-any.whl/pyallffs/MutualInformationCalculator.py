import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class MutualInformationCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_mutual_information(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        mutual_informations = []
        for feature in input_data.columns:
            mi = self.calculate_mi(input_data[feature], output_data)
            mutual_informations.append(mi)

        ranked_features = np.argsort(mutual_informations)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, mutual_informations, feature_names)

        return mutual_informations, ranked_features

    def calculate_mi(self, X, y):
        contingency_table = pd.crosstab(X, y)
        contingency_table = contingency_table.values
        p_xy = contingency_table / float(np.sum(contingency_table)) # Joint probability distribution
        p_x = np.sum(p_xy, axis=1)[:, np.newaxis] # Marginal probability distribution of X
        p_y = np.sum(p_xy, axis=0)[np.newaxis, :] # Marginal probability distribution of y
        p_xy[p_xy == 0] = 1e-12 # Avoid division by zero
        mi = np.sum(p_xy * np.log(p_xy / (p_x * p_y)))
        return mi

    def plot_feature_importance(self, ranked_features, mutual_informations, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), np.array(mutual_informations)[ranked_features], color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Mutual Information')
        plt.title('Mutual Information for Features')
        plt.tight_layout()
        plt.show()
