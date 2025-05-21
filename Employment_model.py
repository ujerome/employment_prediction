import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
import matplotlib.pyplot as plt
import joblib
import os

# Load dataset
df = pd.read_csv(r"C:\Users\uwany\Employment\EDUCATION DATASET.csv")

# Drop unhelpful or unwanted columns
df = df.drop(columns=['pid', 'occupation', 'Contract_duration', 'youngs', 'unemployment_duration'], errors='ignore')

# Convert LFP to binary labels
df['LFP'] = df['LFP'].apply(lambda x: 'Employed' if x == 'Employed' else 'Unemployed')

# Drop rows with any missing values
df = df.dropna()

# Encode categorical columns
label_encoders = {}
for col in df.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target
X = df.drop(columns='LFP')
y = df['LFP']

# Save feature names
FEATURES = X.columns.tolist()

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Predictions and probabilities
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]
class_names = label_encoders['LFP'].classes_

# Classification report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=class_names))

# Create directory to save model and files
os.makedirs("saved_model", exist_ok=True)

# Save model, encoders, and features
joblib.dump(model, "saved_model/logistic_model.joblib")
joblib.dump(label_encoders, "saved_model/label_encoders.joblib")
joblib.dump(FEATURES, "saved_model/features.joblib")

# Confusion matrix plot
cm = confusion_matrix(y_test, y_pred, labels=label_encoders['LFP'].transform(class_names))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig("saved_model/confusion_matrix.png")
plt.close()

# ROC curve
fpr, tpr, _ = roc_curve(y_test, y_prob, pos_label=label_encoders['LFP'].transform(['Employed'])[0])
roc_auc = auc(fpr, tpr)
plt.figure()
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.grid(True)
plt.savefig("saved_model/roc_curve.png")
plt.close()

print("✅ Training complete. Model, encoders, features, and plots saved.")
