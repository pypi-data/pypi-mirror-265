import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

class FilterFeatureSelectionComparison:
    def __init__(self, dataframe, drop_labels, target, methods, test_size=0.20, k_feature=10):
        self.dataframe = dataframe
        self.drop_labels = drop_labels
        self.target = target
        self.methods = methods
        self.test_size = test_size
        self.k_feature = k_feature

    def all_filter_feature_selection_comparison(self):
        results = []

        # Calculate Random Forest classifier performance without feature selection
        X = self.dataframe.drop(labels=self.drop_labels, axis=1)
        y = self.dataframe[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)
        rf = RandomForestClassifier(random_state=42)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred)
        results.append(('Without-Feature-Selection', accuracy, precision, recall, f1, roc_auc))

        # Create a DataFrame to store results
        results_df = pd.DataFrame(columns=['Feature Selection Method', 'Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC AUC'])

        # Apply each feature selection method and save the results
        for method_name in self.methods:
            method_func = getattr(self, method_name)
            _, feature_importances = method_func(self.dataframe, self.drop_labels, self.target, plot_importance=False)
            # Select top k features
            top_k_features = np.argsort(feature_importances)[-self.k_feature:]
            # Train Random Forest classifier with selected features
            rf = RandomForestClassifier(n_estimators=100, random_state=42)
            rf.fit(X_train.iloc[:, top_k_features], y_train)
            # Make predictions
            y_pred = rf.predict(X_test.iloc[:, top_k_features])
            # Calculate evaluation metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_pred)
            results_df = results_df.append({'Feature Selection Method': method_name,
                                            'Accuracy': accuracy,
                                            'Precision': precision,
                                            'Recall': recall,
                                            'F1 Score': f1,
                                            'ROC AUC': roc_auc}, ignore_index=True)

        # Add Without-Feature-Selection results to the DataFrame
        for result in results:
            results_df = results_df.append({'Feature Selection Method': result[0],
                                            'Accuracy': result[1],
                                            'Precision': result[2],
                                            'Recall': result[3],
                                            'F1 Score': result[4],
                                            'ROC AUC': result[5]}, ignore_index=True)

        # Plot results
        plt.figure(figsize=(10, 6))
        results_df_sorted = results_df.sort_values(by='Accuracy', ascending=False)
        bars = plt.bar(results_df_sorted['Feature Selection Method'], results_df_sorted['Accuracy'], color='skyblue')
        bars[0].set_color('green')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Filter Feature Selection Method')
        plt.ylabel('Accuracy')
        plt.title('Comparison of All Filter Feature Selection Methods with Random Forest')
        plt.ylim(0, 1)
        plt.show()

        # Display results sorted by accuracy
        results_df_sorted.to_csv("results.csv")
        print(results_df_sorted)

    def calculate_fisher_score(self, dataframe, drop_labels, target, plot_importance=True):
        pass

    def calculate_t_score(self, dataframe, drop_labels, target, plot_importance=True):
        pass

    # Define other feature selection methods similarly


