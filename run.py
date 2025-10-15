import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Load the iris datasets
iris = load_iris()
X, y = iris.data, iris.target

# Train a random forest classifier
model = RandomForestClassifier()
model.fit(X, y)

# Save trained model
joblib.dump(model, 'app/model.joblib')