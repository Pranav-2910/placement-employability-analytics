# Importing the required libraries for data processing and machine learning
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

# Loading the student placement dataset from the CSV file
df = pd.read_csv("DataSet/train.csv")

# Mapping the Placement_Status column to a binary label (Placed: 1, Not Placed: 0)
df["Placed"] = df["Placement_Status"].map({"Placed": 1, "Not Placed": 0})

# Creating the engineered feature Avg_Skill_Score by averaging three skill ratings
df["Avg_Skill_Score"] = (df["Coding_Skills"] + df["Communication_Skills"] + df["Soft_Skills_Rating"]) / 3.0

# Creating the engineered feature Experience_Score by combining internships, projects, and certifications
df["Experience_Score"] = (df["Internships"] * 2) + df["Projects"] + df["Certifications"]

# Defining the list of features to use for predicting placement
features = [
    "Age", 
    "Gender", 
    "Degree", 
    "Branch", 
    "CGPA", 
    "Internships", 
    "Projects", 
    "Coding_Skills", 
    "Communication_Skills", 
    "Aptitude_Test_Score", 
    "Soft_Skills_Rating", 
    "Certifications", 
    "Backlogs",
    "Avg_Skill_Score",
    "Experience_Score"
]

# Extracting the features (X) and target variable (y) from the dataframe
X = df[features]
y = df["Placed"]

# Identifying the categorical features that need encoding
categorical_features = ["Gender", "Degree", "Branch"]

# Setting up the column transformer to encode categorical columns with OneHotEncoder
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough"
)

# Creating the machine learning pipeline combining the preprocessor and the Random Forest Classifier
# Setting min_samples_leaf=50 to smooth out and calibrate the predicted placement probabilities
model_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, min_samples_leaf=50, random_state=42))
    ]
)

# Splitting the data into training (80%) and validation (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Training the model pipeline on the training dataset
print("Training the Random Forest Classifier...")
model_pipeline.fit(X_train, y_train)

# Predicting the placement status on the validation dataset
y_pred = model_pipeline.predict(X_test)
y_prob = model_pipeline.predict_proba(X_test)[:, 1]

# Evaluating the model performance metrics
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

# Printing the accuracy score and the ROC AUC score
print(f"Model Training Completed!")
print(f"Validation Accuracy: {accuracy:.6f}")
print(f"ROC AUC Score: {roc_auc:.6f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Saving the trained pipeline containing preprocessor and model to a pickle file
print("Saving the trained model pipeline to placement_model.pkl...")
with open("ML Model/placement_model.pkl", "wb") as f:
    pickle.dump(model_pipeline, f)

print("Model successfully saved!")
