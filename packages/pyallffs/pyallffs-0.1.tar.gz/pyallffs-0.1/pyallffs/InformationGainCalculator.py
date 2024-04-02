import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class EntropyCalculator:
    @staticmethod
    def calculate_entropy(y):
        unique, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy

    @staticmethod
    def calculate_conditional_entropy(feature, y):
        unique_values, value_counts = np.unique(feature, return_counts=True)
        conditional_entropy = 0
        total_samples = len(feature)
        for value, count in zip(unique_values, value_counts):
            subset_indices = np.where(feature == value)[0]
            subset_target = y[subset_indices]
            subset_entropy = EntropyCalculator.calculate_entropy(subset_target)
            conditional_entropy += (count / total_samples) * subset_entropy
        return conditional_entropy

class InformationGainCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_information_gain(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns
        X = np.array(input_data)
        y = np.array(output_data)

        entropy_whole = EntropyCalculator.calculate_entropy(y)

        information_gains = []
        for i in range(X.shape[1]):
            information_gains.append(entropy_whole - EntropyCalculator.calculate_conditional_entropy(X[:, i], y))

        ranked_features = np.argsort(information_gains)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, information_gains, feature_names)

        return information_gains, ranked_features

    def plot_feature_importance(self, ranked_features, information_gains, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), np.array(information_gains)[ranked_features], align='center', color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Information Gain')
        plt.title('Information Gain for Features')
        plt.tight_layout()
        plt.show()
