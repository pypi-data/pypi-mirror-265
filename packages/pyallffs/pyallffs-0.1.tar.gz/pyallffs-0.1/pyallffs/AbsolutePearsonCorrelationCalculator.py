import numpy as np
import matplotlib.pyplot as plt

class AbsolutePearsonCorrelationCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_absolute_pearson_correlation(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        correlation_coeffs = self.calculate_correlation_coeffs(input_data, output_data)

        ranked_features = np.argsort(np.abs(correlation_coeffs))[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, correlation_coeffs, feature_names)

        return correlation_coeffs, ranked_features

    def calculate_correlation_coeffs(self, input_data, output_data):
        correlation_coeffs = []
        for feature in input_data.columns:
            correlation = np.corrcoef(input_data[feature], output_data)[0, 1]
            correlation_coeffs.append(correlation)
        return np.array(correlation_coeffs)

    def plot_feature_importance(self, ranked_features, correlation_coeffs, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), np.abs(correlation_coeffs)[ranked_features], align='center', color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Absolute Correlation Coefficient')
        plt.title('Absolute Pearson Correlation Coefficients with Target')
        plt.tight_layout()
        plt.show()
