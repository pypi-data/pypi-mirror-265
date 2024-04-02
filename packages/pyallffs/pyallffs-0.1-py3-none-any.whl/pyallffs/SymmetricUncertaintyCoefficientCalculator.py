import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class SymmetricUncertaintyCoefficientCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_symmetric_uncertainty_coefficient(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        information_gains, _ = InformationGainCalculator(self.dataframe, self.drop_labels, self.target).calculate_information_gain(plot_importance=False)

        symmetric_uncertainty_coefficients = []
        for feature, ig in zip(input_data.columns, information_gains):
            entropy_feature = EntropyCalculator.calculate_entropy(input_data[feature])
            entropy_target = EntropyCalculator.calculate_entropy(output_data)
            symmetric_uncertainty_coefficient = (2 * ig) / (entropy_feature + entropy_target)
            symmetric_uncertainty_coefficients.append(symmetric_uncertainty_coefficient)

        ranked_features = np.argsort(symmetric_uncertainty_coefficients)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, symmetric_uncertainty_coefficients, feature_names)

        return symmetric_uncertainty_coefficients, ranked_features

    def plot_feature_importance(self, ranked_features, symmetric_uncertainty_coefficients, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), np.array(symmetric_uncertainty_coefficients)[ranked_features], align='center', color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Symmetric Uncertainty Coefficient')
        plt.title('Symmetric Uncertainty Coefficient for Features')
        plt.tight_layout()
        plt.show()
