import pandas as pd
import matplotlib.pyplot as plt

class MarkovBlanketCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_markov_blanket_filter(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        markov_blanket = set()

        for feature in input_data.columns:
            if output_data.corr(input_data[feature]) != 0:
                markov_blanket.add(feature)

        for feature in input_data.columns:
            if output_data.corr(input_data[feature]) != 0:
                children = set(input_data.columns[(input_data.corr()[feature] != 0)])
                markov_blanket = markov_blanket.union(children)

        for child in markov_blanket:
            parents = set(input_data.columns[(input_data.corr()[child] != 0)])
            markov_blanket = markov_blanket.union(parents)

        markov_blanket.discard(self.target)

        markov_blanket_sorted = sorted(markov_blanket, key=lambda x: abs(output_data.corr(input_data[x])), reverse=True)
        correlation_values = [output_data.corr(input_data[feature]) for feature in markov_blanket_sorted]
        feature_indices = [feature_names.get_loc(feature) for feature in markov_blanket_sorted]

        if plot_importance:
            self.plot_feature_importance(markov_blanket_sorted, correlation_values)

        return correlation_values, feature_indices

    def plot_feature_importance(self, markov_blanket_sorted, correlation_values):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(markov_blanket_sorted)), correlation_values, color='skyblue')
        plt.xticks(range(len(markov_blanket_sorted)), markov_blanket_sorted, rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Correlation with Target')
        plt.title('Feature Importance (Markov Blanket)')
        plt.tight_layout()
        plt.show()
