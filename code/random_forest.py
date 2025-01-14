import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from scipy.stats import entropy
import numpy as np
from sklearn.tree import export_graphviz
from graphviz import Source

# Load the dataset
file_path = 'output2.txt'

# The dataset is space-delimited and the second column is the classifier
columns = [
    'file_name', 'avg_bpm_normalized', 'avg_rhythmic_density_normalized', 
    'avg_velocity_normalized', 'bpm_std_dev_normalized', 'velocity_std_dev_normalized', 
    'percent_irregular_time_signature'
]

# Read the dataset where the second row (or column in your case) contains the classifier
data = pd.read_csv(file_path, sep=' ', header=None, names=columns, engine='python')

# Assuming the second row corresponds to the 'classifier' column
# Add classifier column (if classifier is in the second row, shift and assign it)
data['classifier'] = data.iloc[:, 1]  # Assuming the classifier is in the second column (change if necessary)

# Remove the classifier from feature columns, leaving just the features
X = data.drop(columns=['file_name', 'classifier'])

# Now assume that the 'classifier' is the label
y = data['classifier']

# Handle missing values by imputing with the median
X.fillna(X.median(numeric_only=True), inplace=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=y.unique())

# Calculate Information Gain from the entire dataset
class_probabilities = y.value_counts(normalize=True)
initial_entropy = entropy(class_probabilities, base=2) #calculated with the base entrophy formula, manually checked in paper

predicted_probabilities = model.predict_proba(X_test)
predicted_entropy = np.mean([entropy(probs, base=2) for probs in predicted_probabilities])

information_gain = initial_entropy - predicted_entropy

# Print results
print("Accuracy:", accuracy)
print("Classification Report:\n", report)
print("Initial Entropy:", initial_entropy)
print("Predicted Entropy:", predicted_entropy)
print("Information Gain:", information_gain)