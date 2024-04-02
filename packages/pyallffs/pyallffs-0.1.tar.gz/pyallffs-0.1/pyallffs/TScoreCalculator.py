import numpy as np
import matplotlib.pyplot as plt

class TScoreCalculator:
    def __init__(self, dataframe, drop_labels, target):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target

    def calculate_t_score(self, plot_importance=True):
        input_data = self.dataframe.drop(labels=self.drop_labels, axis=1)
        output_data = self.dataframe[self.target]
        feature_names = input_data.columns
        X = np.array(input_data)
        y = np.array(output_data)

        unique_classes = np.unique(y)
        if len(unique_classes) != 2:
            raise ValueError("Target variable must have exactly 2 unique classes.")

        mean_class1 = np.mean(X[y == unique_classes[0]], axis=0)
        mean_class2 = np.mean(X[y == unique_classes[1]], axis=0)
        std_class1 = np.std(X[y == unique_classes[0]], axis=0)
        std_class2 = np.std(X[y == unique_classes[1]], axis=0)
        n1 = np.sum(y == unique_classes[0])
        n2 = np.sum(y == unique_classes[1])

        t_scores = np.abs((mean_class1 - mean_class2) / np.sqrt((std_class1**2 / n1) + (std_class2**2 / n2)))

        ranked_features = np.argsort(t_scores)[::-1]

        if plot_importance:
            self.plot_feature_importance(ranked_features, t_scores, feature_names)

        return t_scores, ranked_features

    def plot_feature_importance(self, ranked_features, t_scores, feature_names):
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(ranked_features)), t_scores[ranked_features], align='center', color='skyblue')
        plt.xticks(range(len(ranked_features)), [feature_names[i] for i in ranked_features], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('T-Score')
        plt.title('T-Score for Features')
        plt.tight_layout()
        plt.show()
