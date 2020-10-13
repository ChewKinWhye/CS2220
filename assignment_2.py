import os
from utils.assignment2.data import count_ALL_subtype, count_genes, common_genes, clean_and_merge
from sklearn.feature_selection import chi2
from sklearn import tree, svm
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score


train_label_file_path = os.path.join("Dataset", "Assignment2", "training", "trainset10-02-01annotation.xls")
test_label_file_path = os.path.join("Dataset", "Assignment2", "testing", "testset10-02-01annotation.xls")
train_data_directory = os.path.join("Dataset", "Assignment2", "training", "trainset10-02-01")
test_data_directory = os.path.join("Dataset", "Assignment2", "testing", "testset10-02-01")

print(f"Number of ALL-subtype training samples: {count_ALL_subtype(train_label_file_path)}")
print(f"Number of ALL-subtype test samples: {count_ALL_subtype(test_label_file_path)}")

total_gene_count = []
total_gene_count.extend(count_genes(train_data_directory))
total_gene_count.extend(count_genes(test_data_directory))
for gene_count in total_gene_count:
    if gene_count != 12610:
        print("Not all the same")
        break
# This else statement is executed if the for loop completes (Does not break)
else:
    print("All files have 12610 genes")

common_train_genes = common_genes(train_data_directory)
common_test_genes = common_genes(test_data_directory)
common_combined_genes = list(common_train_genes.intersection(common_test_genes))
print(f"Number of genes left: {len(common_combined_genes)}")
train_x, train_y = clean_and_merge(train_data_directory, train_label_file_path, common_combined_genes, "train.csv")
test_x, test_y = clean_and_merge(test_data_directory, test_label_file_path, common_combined_genes, "test.csv")

chi_values, pval = chi2(train_x, train_y)
chi2_top_index = chi_values.argsort()[::-1]

top_200_genes = [common_combined_genes[i] for i in chi2_top_index[0:200]]
chi_values.sort()
chi_values = chi_values[::-1]
top_200_values = chi_values[0:200]
print(f"Top 200 genes: {top_200_genes}")
print(f"Top 200 values: {top_200_values}")

print(f"Shape of training data {train_x.shape}")
train_x = train_x[:, np.array(chi2_top_index[0:200])]
test_x = test_x[:, np.array(chi2_top_index[0:200])]

print(f"Shape of feature-selected training data {train_x.shape}")

decision_tree = tree.DecisionTreeClassifier()
decision_tree.fit(train_x, train_y)
y_predictions = decision_tree.predict(test_x)
print(f"Decision Tree confusion matrix: {confusion_matrix(test_y, y_predictions)}")
print(f"Decision Tree accuracy: {accuracy_score(test_y, y_predictions)}")
svm_model = svm.SVC()
svm_model.fit(train_x, train_y)
y_predictions = svm_model.predict(test_x)
print(f"SVM confusion matrix: {confusion_matrix(test_y, y_predictions)}")
print(f"SVM accuracy: {accuracy_score(test_y, y_predictions)}")
