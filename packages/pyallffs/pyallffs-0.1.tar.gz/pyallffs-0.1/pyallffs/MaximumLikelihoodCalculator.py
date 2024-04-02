import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class MaximumLikelihoodCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_maximum_likelihood_feature_selection(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        model = LinearRegression()
        model.fit(input_data, output_data)

        coefficients = model.coef_

        ranked_features = np.argsort(np.abs(coefficients))[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, coefficients, feature_names)

        return coefficients, ranked_features

    def plot_feature_importance(self, ranked_features, coefficients, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), np.abs(coefficients[ranked_features]), color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Coefficient Magnitude')
        plt.ylabel('Features')
        plt.title('Feature Importance (Maximum Likelihood)')
        plt.tight_layout()
        plt.show()
