from utils.assignment1.data import extract_arff_data
from utils.assignment1.evaluate import evaluation_metrics_binary

from sklearn import tree, svm
from sklearn.feature_selection import chi2
from sklearn.model_selection import KFold


if __name__ == "__main__":
    x, y = extract_arff_data()
    kf = KFold(n_splits=10, shuffle=True)
    decision_tree_sensitivity, decision_tree_precision, decision_tree_accuracy = 0, 0, 0
    decision_tree_depth, decision_tree_leaves = 0, 0
    svm_tree_sensitivity, svm_tree_precision, svm_tree_accuracy = 0, 0, 0

    for train_index, test_index in kf.split(x):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]

        decision_tree = tree.DecisionTreeClassifier()
        decision_tree.fit(x_train, y_train)
        y_predictions = decision_tree.predict(x_test)
        sensitivity, precision, accuracy = evaluation_metrics_binary(y_test, y_predictions)

        decision_tree_sensitivity += sensitivity
        decision_tree_precision += precision
        decision_tree_accuracy += accuracy
        decision_tree_depth += decision_tree.get_depth()
        decision_tree_leaves += decision_tree.get_n_leaves()

        chi_values, pval = chi2(x_train, y_train)
        chi2_top_index = chi_values.argsort()[::-1]
        x_train_svm = x_train[:, chi2_top_index[0:10]]
        x_test_svm = x_test[:, chi2_top_index[0:10]]
        svm_model = svm.SVC()
        svm_model.fit(x_train_svm, y_train)
        y_predictions = svm_model.predict(x_test_svm)
        sensitivity, precision, accuracy = evaluation_metrics_binary(y_test, y_predictions)
        svm_tree_sensitivity += sensitivity
        svm_tree_precision += precision
        svm_tree_accuracy += accuracy

    print(f"DT recall: {decision_tree_sensitivity/10}\nDT precision: {decision_tree_precision/10}"
          f"\nDT accuracy: {decision_tree_accuracy/10}")
    print(f"Depth: {int(decision_tree_depth/10)}\nLeaves:{int(decision_tree_leaves/10)}")
    print(f"SVM recall: {svm_tree_sensitivity / 10}\nSVM precision: {svm_tree_precision / 10}"
          f"\nSVM accuracy: {svm_tree_accuracy / 10}")

