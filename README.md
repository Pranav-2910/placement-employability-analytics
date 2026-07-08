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
1. **`Avg_Skill_Score`**: Calculated as the average of the student's primary skill ratings:
   $$\text{Avg Skill Score} = \frac{\text{Coding Skills} + \text{Communication Skills} + \text{Soft Skills Rating}}{3}$$
2. **`Experience_Score`**: Calculated as a combination of internships, projects, and certifications:
   $$\text{Experience Score} = (\text{Internships} \times 2) + \text{Projects} + \text{Certifications}$$
3. **`Employability_Score`** (SQL query 6 formulation):
   $$\text{Employability Score} = (0.4 \times \text{Avg Skill Score}) + (0.3 \times \text{Experience Score}) + (0.2 \times \text{Aptitude Test Score}) + (0.1 \times \text{Soft Skills Rating})$$

---

<!-- Documenting the step-by-step workflow and methodology -->
## 🔄 Project Workflow & Methodology

The project was executed through the following structured phases:

### 1. Data Cleaning & Preprocessing
*   **Missing Value Check**: Loaded the raw dataset `train.csv` and verified that there were zero missing values across all 45,000 student records.
*   **Target Encoding**: Converted the categorical `Placement_Status` column into a binary label column named `Placed` (`Placed` = 1, `Not Placed` = 0) to prepare it for machine learning classification.
*   **Feature Engineering**: Created custom columns `Avg_Skill_Score` and `Experience_Score` using pandas to construct robust indicators of academic and practical competency.
*   **Exporting Data**: Exported the processed data as `cleaned_placement_data.csv` inside the `Python Analysis` folder for database ingestion and visualization.

### 2. Exploratory Data Analysis (EDA)
*   **Feature Distribution**: Inspected value counts and distribution shapes for demographics (gender splits were roughly 50-50), degrees, and engineering branches.
*   **Correlation Analysis**: Computed correlation coefficients of numerical attributes with placement status.
    *   **Key Positive Drivers**: `Projects` ($r \approx 0.50$), `CGPA` ($r \approx 0.49$), `Certifications` ($r \approx 0.47$), and `Coding_Skills` ($r \approx 0.44$).
    *   **Key Negative Driver**: `Backlogs` ($r \approx -0.49$), proving that active backlogs are the primary filter used by campus recruiters.

### 3. SQL Analytics
*   **Database Ingestion**: Created a relational database named `placement_analysis_db` and imported the student records.
*   **Descriptive Statistics**: Wrote and executed SQL queries to calculate overall placement rates, success rates grouped by engineering branch and degree types, and average CGPA metrics of placed vs. unplaced students.
*   **Employability Scoring**: Formulated queries to calculate a multi-dimensional `employability_score` for each student based on weighted parameters, and ranked students using SQL window functions (`RANK() OVER`).

### 4. Power BI Dashboarding
*   **Data Connection**: Ingested the cleaned dataset into Power BI.
*   **Interactive Visuals**: Created key metric cards, demographic breakdowns, department-wise placement success trends, and skill distribution charts. This interactive dashboard enables academic decision-makers to track student progress and placement readiness.

### 5. Machine Learning Modeling
*   **Algorithm Evaluation**: Trained and evaluated several candidate classification models (Decision Trees, Random Forest, XGBoost, and LightGBM) to find the most accurate classifier.
*   **Model Selection & Calibration**: Deployed a **Random Forest Classifier** as the production model. We configured it with `min_samples_leaf=50` to regularize and calibrate predictions. This ensures the web application outputs a smooth, continuous placement probability (%) instead of abrupt binary jumps.
*   **Serialization**: Saved the preprocessing and model steps into a scikit-learn `Pipeline` and serialized it to `ML Model/placement_model.pkl` for Streamlit deployment.

### 6. Streamlit Web Application
*   **Interface Design**: Built a modern dark-themed web app featuring dual modes: a **Student Predictor & Profiler** and a **Recruiter Batch Prediction Portal**.
*   **Interactive Analytics**: Connected user input sliders to the ML pipeline to yield real-time predictions, placement probability gauge charts, and skill comparison radar charts.
*   **Dynamic Advices**: Designed an automated career advice system that provides actionable, tailored steps to students (e.g. suggesting backlog clearance, certification completion, or coding practices) depending on their input values.

---

<!-- Describing the machine learning model selection and calibration -->
## 🤖 Machine Learning Model Performance

During our **research and model selection phase**, we evaluated multiple classification models on a 20% test split to find the best predictor:

*   **Standard Random Forest Classifier**: 100.0% Validation Accuracy (ROC AUC: 1.0)
*   **LightGBM Classifier**: 100.0% Validation Accuracy (ROC AUC: 1.0)
*   **XGBoost Classifier**: 99.97% Validation Accuracy (ROC AUC: 1.0)
*   **Calibrated Random Forest Classifier** (Deployed): **99.83% Validation Accuracy** (ROC AUC: 1.0)

> [!NOTE]
> Since the dataset is noiseless and synthetic, standard tree-based classifiers learn the decision boundaries perfectly, leading to binary probability outputs (exactly 0.0% or 100.0%). We chose to deploy the **Calibrated Random Forest Classifier** (`min_samples_leaf=50`). This regularization smooths the model's leaf node distributions, allowing the Streamlit application to output continuous probability estimates (e.g., 72.5%) that react naturally as users adjust the sliders, while maintaining near-perfect accuracy.

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
