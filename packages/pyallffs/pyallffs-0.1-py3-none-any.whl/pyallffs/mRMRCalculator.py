import numpy as np
import matplotlib.pyplot as plt

class mRMRCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_mrmr(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns

        relevance_scores = self.calculate_relevance_scores(input_data, output_data)
        redundancy_scores = self.calculate_redundancy_scores(input_data)

        mrmr_scores = relevance_scores - np.mean(redundancy_scores, axis=1)

        ranked_features = np.argsort(mrmr_scores)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, mrmr_scores, feature_names)

        return mrmr_scores, ranked_features

    def calculate_relevance_scores(self, input_data, output_data):
        relevance_scores = []
        for feature in input_data.columns:
            relevance_scores.append(self.calculate_relevance(input_data[feature], output_data))
        return np.array(relevance_scores)

    def calculate_relevance(self, feature, target):
        correlation = np.abs(np.corrcoef(feature, target)[0, 1])
        return correlation

    def calculate_redundancy_scores(self, input_data):
        redundancy_scores = []
        for feature1 in input_data.columns:
            redundancy_scores.append([self.calculate_redundancy(input_data[feature1], input_data[feature2]) for feature2 in input_data.columns])
        return np.array(redundancy_scores)

    def calculate_redundancy(self, feature1, feature2):
        correlation = np.abs(np.corrcoef(feature1, feature2)[0, 1])
        return correlation

    def plot_feature_importance(self, ranked_features, mrmr_scores, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), mrmr_scores[ranked_features], align='center', color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('mRMR Score')
        plt.title('mRMR Score for Features')
        plt.tight_layout()
        plt.show()
