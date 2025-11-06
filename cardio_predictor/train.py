import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv("Medicaldataset.csv")

# Encode the target
df['Result'] = df['Result'].map({'negative': 0, 'positive': 1})

# Features and target
X = df.drop('Result', axis=1)
y = df['Result']

# Feature Scaling (Optional for RandomForest, but improves consistency)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Save model and scaler
joblib.dump(model, 'heart_attack_model.pkl')
joblib.dump(scaler, 'scalerrr.pkl')
