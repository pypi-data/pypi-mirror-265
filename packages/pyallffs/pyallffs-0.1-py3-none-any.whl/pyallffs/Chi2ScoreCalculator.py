import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_selection import chi2

class Chi2ScoreCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_chi2_score(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        input_data = input_data.apply(lambda x: pd.factorize(x)[0])
        X = np.array(input_data)
        y = np.array(output_data)

        chi2_scores, _ = chi2(X, y)

        ranked_features = np.argsort(chi2_scores)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, chi2_scores, feature_names)

        return chi2_scores, ranked_features

    def plot_feature_importance(self, ranked_features, chi2_scores, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), chi2_scores[ranked_features], align='center', color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Chi-Squared Score')
        plt.title('Chi-Squared Score for Features')
        plt.tight_layout()
        plt.show()
