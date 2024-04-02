# KNN Classifier

**A k-Nearest Neighbors supervised classifier in Python 3.11.7**

---

# Importing the package

```bash
pip install knnclassifier
```

```python
from knnclassifier import KNNClassifier
```

This statement imports the `KNNClassifier` class, which will be used to create your classifier objects.

# Using the package

## Fitting the classifier

_Set up your training and test data and fit the classifier._

1. Populate two text files with your training and test data.

> 1.4, 4.0, 15.0, 1.1, 1.6, 5.0\
> 1.2, 4.0, 22.2, 2.2, 3.0, 6.0\
> ...

Each line serves as a record and contains a list of its data points (fields), with the record's label as the final item
in the list. In the above examples, the labels are 5.0 and 6.0, respectively. Ensure that fields are separated by a
consistent **delimiter** (e.g., a comma and a space).

2. Split the data and label arrays from the files.

```python
train_data, train_label = KNNClassifier.split_data_label_from_file("train.txt", delimiter=", ")
test_data, actual_label = KNNClassifier.split_data_label_from_file("test.txt", delimiter=", ")
```

The static method `split_data_label_from_file` returns two numpy arrays. The first contains all columns except the
last (the **data** columns), and the second contains the last column (the **label** column).

You may also specify the `delimiter`. By default, it is `", "`, but you may specify any string.

3. Initialize a `KNNClassifier` object and fit it to the training arrays.

```python
classifier = KNNClassifier()
classifier.fit(train_data, train_label)
```

## Making and checking predictions with the classifier

1. Compute and store label predictions for the test data.

```python
test_label_predictions = classifier.predict(test_data, k=5)
```

The `predict` method returns the predicted labels of each record of the test data. Specify the k value to be used during
prediction.

> [!NOTE]
> Ensure that the test data has the same number of fields (columns) as the training data. This is required for the
> algorithm to function correctly.

2. Check the accuracy of the label predictions.

```python
accuracy: float = KNNClassifier.check_accuracy(test_label_predictions, actual_label, print_info=False)
```

The static method `check_accuracy` returns the proportion of the predicted labels that match the actual labels.

You may also specify `print_info` (default: False). If set to True, each label will be printed individually.
