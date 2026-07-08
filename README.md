<!-- Describing the Student Placement & Employability Analysis project -->
# Student Placement & Employability Analysis

An end-to-end data analytics and predictive modeling project that analyzes student profiles and predicts placement outcomes using machine learning.

The repository integrates SQL query analytics, Jupyter data cleaning notebooks, an interactive Power BI dashboard, a high-accuracy calibrated Random Forest classification model, and a premium Streamlit web application.

---

<!-- Outlining the feature engineering and data dictionary -->
## 📊 Dataset & Feature Engineering

The dataset consists of **45,000 student records** containing academic, cognitive, and experience metrics:

| Feature Name | Type | Description |
| :--- | :--- | :--- |
| `Age` | Numerical | Age of the student (18 to 24) |
| `Gender` | Categorical | Male or Female |
| `Degree` | Categorical | B.Tech, BCA, MCA, B.Sc |
| `Branch` | Categorical | CSE, IT, ECE, ME, Civil |
| `CGPA` | Numerical | Cumulative Grade Point Average (out of 10) |
| `Internships` | Numerical | Number of internships completed |
| `Projects` | Numerical | Number of projects completed |
| `Coding_Skills` | Numerical | Technical coding rating (1 to 10) |
| `Communication_Skills` | Numerical | Verbal communication rating (1 to 10) |
| `Aptitude_Test_Score` | Numerical | Quantitative aptitude screening score (0 to 100) |
| `Soft_Skills_Rating` | Numerical | Personal skills rating (1 to 10) |
| `Certifications` | Numerical | Count of professional certifications earned |
| `Backlogs` | Numerical | Number of active or historical backlogs |

### 🛠️ Engineered Columns:
1. **`Avg_Skill_Score`**: Calculated as:
   $$\text{Avg\_Skill\_Score} = \frac{\text{Coding\_Skills} + \text{Communication\_Skills} + \text{Soft\_Skills\_Rating}}{3}$$
2. **`Experience_Score`**: Calculated as:
   $$\text{Experience\_Score} = (\text{Internships} \times 2) + \text{Projects} + \text{Certifications}$$
3. **`Employability_Score`** (SQL query 6 formulation):
   $$\text{Employability\_Score} = (0.4 \times \text{Avg\_Skill\_Score}) + (0.3 \times \text{Experience\_Score}) + (0.2 \times \text{Aptitude\_Test\_Score}) + (0.1 \times \text{Soft\_Skills\_Rating})$$

---

<!-- Highlighting model evaluation and training metrics -->
## 🤖 Machine Learning Model Performance

We trained classification algorithms to predict placement status (`Placement_Status` -> `Placed` = 1, `Not Placed` = 0) and evaluate their performance on an independent 20% test split:

- **Calibrated Random Forest Classifier** (with `min_samples_leaf=50`): **99.83% Accuracy** (ROC AUC: 1.0)
- **Standard Random Forest Classifier**: **100% Accuracy** (ROC AUC: 1.0)
- **LightGBM Classifier**: **100% Accuracy** (ROC AUC: 1.0)
- **XGBoost Classifier**: **99.97% Accuracy** (ROC AUC: 1.0)

We deployed the **Calibrated Random Forest Classifier Pipeline** which bundles categorical one-hot encoding (`Gender`, `Degree`, `Branch`). This model is optimized to provide smooth, continuous placement probabilities (e.g. 74.5%) instead of binary jumps, making it highly responsive to small changes in input parameters while retaining near-perfect accuracy.

---

<!-- Detailing the features of the Streamlit Web Application -->
## 💻 Streamlit Web Application Features

The interactive dashboard (`app.py`) is styled with a custom dark-themed glassmorphism UI:

1. **Student Predictor & Profiler**:
   - Slide input controls to configure student academic, skill, and experience details.
   - Real-time prediction status (Placed vs. Not Placed).
   - Placement confidence level (%) and raw Employability Score.
2. **Personalized Career Correction & Action Plan**:
   - Rendered directly below the outputs to provide immediate feedback.
   - Generates smart suggestions on how to improve placement chances (e.g. advising to clear backlogs, boost CGPA, add certifications, or improve coding).
3. **Interactive Visualizations**:
   - **Radar Chart**: Compares the entered profile against the benchmark average of placed students in the same branch.
   - **Gauge Chart**: Displays the probability of placement in a color-coded speed dial.
4. **Recruiters Portal**:
   - Batch upload capability using CSV files.
   - Summarizes prediction outcomes, calculates employability scores for all rows, and plots batch statistics (placements bar chart and branch employability box plots).
   - Export option to download the completed predictions report.

---

<!-- Explaining how to launch the Streamlit application -->
## 🚀 How to Run the App

Follow these steps to run the application on your local machine:

### 1. Install Requirements
Ensure python is installed on your computer. Run the following command in your terminal to install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Server
Launch the application by running:
```bash
streamlit run app.py
```
This will automatically open the dashboard in your default browser.
