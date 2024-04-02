import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class GainRatioCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_gain_ratio(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns
        X = np.array(input_data)
        y = np.array(output_data)

        information_gains, _ = InformationGainCalculator(self.dataframe, self.drop_labels, self.target).calculate_information_gain(plot_importance=False)

        split_information = []
        for i in range(X.shape[1]):
            split_information.append(self.calculate_split_information(X[:, i]))

        gain_ratios = np.array(information_gains) / np.array(split_information)

        ranked_features = np.argsort(gain_ratios)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, gain_ratios, feature_names)

        return gain_ratios, ranked_features

    def calculate_split_information(self, feature):
        unique_values, counts = np.unique(feature, return_counts=True)
        probabilities = counts / len(feature)
        split_information = -np.sum(probabilities * np.log2(probabilities))
        return split_information

    def plot_feature_importance(self, ranked_features, gain_ratios, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), gain_ratios[ranked_features], align='center', color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Gain Ratio')
        plt.title('Gain Ratio for Features')
        plt.tight_layout()
        plt.show()
