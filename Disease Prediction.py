# ==============================
# SIH Project: PredictWell Prototype
# Disease Prediction from Medication & Test Results
# ==============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from matplotlib.backends.backend_pdf import PdfPages
import joblib

# ==============================
# 1. Load Dataset
# ==============================
df = pd.read_csv("healthcare_dataset.csv")

# Using Medication + Test Results as features, Medical Condition as target
df = df.dropna(subset=["Medication", "Test Results", "Medical Condition"])
df["combined_text"] = df["Medication"].astype(str) + " || " + df["Test Results"].astype(str)
X = df["combined_text"]
y = df["Medical Condition"]

# Encode labels
le = LabelEncoder()
y_enc = le.fit_transform(y)

# ==============================
# 2. Train/Test Split
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

# ==============================
# 3. Build Pipeline (TF-IDF + Logistic Regression)
# ==============================
pipe = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
    ("clf", LogisticRegression(max_iter=1000, multi_class="ovr"))
])

param_grid = {"clf__C": [0.1, 1, 10]}
grid = GridSearchCV(pipe, param_grid, cv=3, scoring="accuracy", verbose=1, n_jobs=-1)
grid.fit(X_train, y_train)

best = grid.best_estimator_

# ==============================
# 4. Evaluate
# ==============================
y_pred = best.predict(X_test)
y_proba = best.predict_proba(X_test)
acc = accuracy_score(y_test, y_pred)

print("Best Params:", grid.best_params_)
print("Test Accuracy:", acc)

# Save model + label encoder
joblib.dump(best, "disease_model.joblib")
joblib.dump(le, "label_encoder.joblib")

# ==============================
# 5. Create Graphs & Save to PDF
# ==============================
pdf_path = "disease_prediction_report.pdf"
pdf = PdfPages(pdf_path)

# 5.1 Accuracy Bar
plt.figure(figsize=(6,4))
plt.bar(["Model Accuracy","Random Baseline"], [acc, 1/len(le.classes_)])
plt.title("Overall Accuracy vs Random Baseline")
plt.ylabel("Accuracy")
pdf.savefig(); plt.close()

# 5.2 Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=False, cmap="Blues", xticklabels=le.classes_, yticklabels=le.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
pdf.savefig(); plt.close()

# 5.3 Precision/Recall/F1 per class
prec, rec, f1, sup = precision_recall_fscore_support(y_test, y_pred, labels=np.arange(len(le.classes_)))
metrics_df = pd.DataFrame({
    "Class": le.classes_,
    "Precision": prec,
    "Recall": rec,
    "F1-score": f1,
    "Support": sup
})
metrics_melt = metrics_df.melt(id_vars="Class", value_vars=["Precision","Recall","F1-score"], 
                               var_name="Metric", value_name="Score")
plt.figure(figsize=(10,6))
sns.barplot(data=metrics_melt, x="Class", y="Score", hue="Metric")
plt.title("Per-class Precision, Recall, F1-score")
plt.xticks(rotation=45)
plt.ylim(0,1)
pdf.savefig(); plt.close()

# 5.4 Support Distribution
plt.figure(figsize=(8,5))
sns.barplot(x="Class", y="Support", data=metrics_df)
plt.title("Support (Number of Test Samples per Class)")
plt.xticks(rotation=45)
pdf.savefig(); plt.close()

# 5.5 Probability distributions for random samples
sample_idxs = np.random.choice(len(X_test), 3, replace=False)
for idx in sample_idxs:
    probs = y_proba[idx]
    plt.figure(figsize=(8,4))
    sns.barplot(x=le.classes_, y=probs)
    plt.title(f"Sample text: {X_test.iloc[idx][:40]}...\nTrue: {le.inverse_transform([y_test[idx]])[0]}, Pred: {le.inverse_transform([y_pred[idx]])[0]}")
    plt.xticks(rotation=45)
    plt.ylabel("Probability")
    pdf.savefig(); plt.close()

# ==============================
# 6. Close PDF Report
# ==============================
pdf.close()
print(f"✅ Report saved as {pdf_path}")
