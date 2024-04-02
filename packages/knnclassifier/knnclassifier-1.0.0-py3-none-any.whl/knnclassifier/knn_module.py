from statistics import mode
import numpy as np


class KNNClassifier:
    def __init__(self):
        """Initialize the classifier."""
        self.fit_data = None
        self.fit_label = None

    def fit(self, training_data: np.ndarray, training_label: np.ndarray):
        """Fit the classifier with the training arrays."""
        self.fit_data = training_data
        self.fit_label = training_label

    def predict(self, test_data, k: int) -> np.ndarray:
        """Return the predicted labels of the test data based on the training data."""

        # Classifier must be trained.
        if self.fit_data is None or self.fit_label is None:
            raise Exception("Classifier is untrained, cannot predict labels. (Remember to fit your classifier)")

        # k must be grater than 0.
        if k < 1:
            raise Exception("k value must be greater than 0.")

        # Initialize prediction array.
        predictions: np.ndarray = np.zeros(len(test_data))

        # Compute a label prediction for each item in test_data.
        for i, datum in enumerate(test_data):
            distances: np.ndarray = np.linalg.norm(datum - self.fit_data, axis=1)
            sorted_indices = np.argsort(distances)
            votes: list = [self.fit_label[i] for i in sorted_indices[:k]]
            predictions[i] = mode(votes)

        return predictions

    @staticmethod
    def check_accuracy(predicted_labels: np.ndarray, actual_labels: np.ndarray, print_info: bool = False) -> float:
        """Return the proportion of the predicted labels that match the actual labels (represented as a decimal)."""

        # Label arrays must be defined.
        if predicted_labels is None or actual_labels is None:
            raise Exception("Label arrays cannot be None.")

        # Label arrays must have the same length.
        if len(predicted_labels) != len(actual_labels):
            raise Exception("Unequal array lengths; cannot check accuracy")

        count: int = np.sum(np.equal(predicted_labels, actual_labels))

        # Print accuracy for each prediction as requested.
        if print_info:
            for i, (predicted, actual) in enumerate(zip(predicted_labels, actual_labels)):
                print(f"Index: {i}, Prediction: {predicted}, Actual: {actual}")
            print(f"Correctly predicted {count} out of {len(predicted_labels)} labels.")

        return count / len(predicted_labels)

    @staticmethod
    def split_data_label_from_file(file_path: str, delimiter: str = ", "):
        """Return the data and label arrays from a file."""

        try:
            with open(file_path, "r") as fileio:
                lines: list[str] = fileio.readlines()

                # Data array contains all but last column.
                data = np.array(
                    [list(map(float, line.split(delimiter)[:-1])) for line in lines],
                    dtype=float
                )

                # Label array contains last column.
                label = np.array(
                    [int(line.split(delimiter)[-1]) for line in lines],
                    dtype=float
                )

                return data, label

        except Exception as e:
            print(type(e).__name__, e)
            return None
