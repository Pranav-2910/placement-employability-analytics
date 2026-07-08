# Importing the required libraries for web application design, data manipulation, and visualization
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px

# Setting up the page configuration for the Streamlit dashboard
st.set_page_config(
    page_title="Student Placement & Employability Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Applying custom CSS styles to create a premium dark-themed, glassmorphic layout
st.markdown("""
<style>
    /* Styling the main container and backgrounds */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #161b22 100%);
        color: #c9d1d9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Styling the cards and panels */
    .metric-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(56, 139, 253, 0.4);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #58a6ff;
        box-shadow: 0 6px 25px rgba(56, 139, 253, 0.3);
    }
    
    /* Styling headers and custom colors */
    .gradient-text {
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Designing status badges */
    .badge-placed {
        background-color: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        border: 1px solid rgba(46, 160, 67, 0.4);
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .badge-unplaced {
        background-color: rgba(248, 81, 73, 0.15);
        color: #ff7b72;
        border: 1px solid rgba(248, 81, 73, 0.4);
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Formatting recommendations section */
    .reco-box {
        background: rgba(33, 38, 45, 0.8);
        border-left: 4px solid #bc8cff;
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Loading the cleaned dataset to compute comparison metrics and averages
@st.cache_data
def load_and_prepare_data():
    # Reading the cleaned student placement data directly using pandas
    df_cleaned = pd.read_csv("Python Analysis/cleaned_placement_data.csv")
    return df_cleaned

# Loading the trained machine learning pipeline
@st.cache_resource
def load_trained_model():
    # Opening the serialized pickle model file and loading it
    with open("ML Model/placement_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

# Initializing data and model variables
df_data = load_and_prepare_data()
placement_model = load_trained_model()

# Rendering the sidebar input elements for entering the student profile
st.sidebar.markdown("<h2 class='gradient-text'>Student Input Profile</h2>", unsafe_allow_html=True)
st.sidebar.write("Configure the parameters below to evaluate placement probability.")

# Designing sidebar sections
st.sidebar.markdown("### 📝 Personal Details")
input_age = st.sidebar.slider("Age", min_value=18, max_value=24, value=21, step=1)
input_gender = st.sidebar.selectbox("Gender", options=["Female", "Male"])

st.sidebar.markdown("### 🎓 Academic Profile")
input_degree = st.sidebar.selectbox("Degree Type", options=sorted(df_data["Degree"].unique()))
input_branch = st.sidebar.selectbox("Branch / Specialization", options=sorted(df_data["Branch"].unique()))
input_cgpa = st.sidebar.slider("Cumulative GPA (CGPA)", min_value=1.0, max_value=10.0, value=7.2, step=0.1)
input_backlogs = st.sidebar.slider("Active/History Backlogs", min_value=0, max_value=5, value=0, step=1)

st.sidebar.markdown("### 🛠️ Practical Experience")
input_internships = st.sidebar.slider("Number of Internships", min_value=0, max_value=5, value=1, step=1)
input_projects = st.sidebar.slider("Number of Projects Done", min_value=0, max_value=10, value=3, step=1)
input_certifications = st.sidebar.slider("Certifications Completed", min_value=0, max_value=10, value=2, step=1)

st.sidebar.markdown("### 🧠 Cognitive & Technical Skills")
input_coding = st.sidebar.slider("Coding Skills Rating", min_value=1, max_value=10, value=6, step=1)
input_comm = st.sidebar.slider("Communication Skills Rating", min_value=1, max_value=10, value=6, step=1)
input_aptitude = st.sidebar.slider("Aptitude Test Score", min_value=0, max_value=100, value=70, step=5)
input_soft = st.sidebar.slider("Soft Skills Rating", min_value=1, max_value=10, value=6, step=1)

# Displaying main dashboard tabs
tab_individual, tab_batch = st.tabs(["🎯 Placement Predictor & Profiler", "📊 Recruiters Portal & Batch Prediction"])

with tab_individual:
    # Creating header for the individual prediction tab
    st.markdown("<h1 class='gradient-text'>Student Placement & Employability Intelligence</h1>", unsafe_allow_html=True)
    st.write("An advanced predictive analytics platform leveraging machine learning to model student placement outcomes.")
    
    st.markdown("---")
    
    # Calculating engineered features identical to the training dataset preprocessing
    avg_skill = (input_coding + input_comm + input_soft) / 3.0
    exp_score = (input_internships * 2) + input_projects + input_certifications
    
    # Creating a single-row dataframe matching the training features format
    input_df = pd.DataFrame([{
        "Age": input_age,
        "Gender": input_gender,
        "Degree": input_degree,
        "Branch": input_branch,
        "CGPA": input_cgpa,
        "Internships": input_internships,
        "Projects": input_projects,
        "Coding_Skills": input_coding,
        "Communication_Skills": input_comm,
        "Aptitude_Test_Score": input_aptitude,
        "Soft_Skills_Rating": input_soft,
        "Certifications": input_certifications,
        "Backlogs": input_backlogs,
        "Avg_Skill_Score": avg_skill,
        "Experience_Score": exp_score
    }])
    
    # Predicting the probability and placement outcome using the loaded model pipeline
    prediction_prob = placement_model.predict_proba(input_df)[0][1]
    prediction_class = placement_model.predict(input_df)[0]
    
    # Calculating the employability score using the SQL weightings formula
    # Formula: 0.4 * Avg_Skill_Score + 0.3 * Experience_Score + 0.2 * Aptitude_Test_Score + 0.1 * Soft_Skills_Rating
    # Max possible: (0.4 * 10) + (0.3 * 20) + (0.2 * 100) + (0.1 * 10) = 4 + 6 + 20 + 1 = 31 (experience score max is 2*5 + 10 + 10 = 30 theoretically)
    # Let's show the raw score out of its direct theoretical maximum based on user inputs
    raw_emp_score = (0.4 * avg_skill) + (0.3 * exp_score) + (0.2 * input_aptitude) + (0.1 * input_soft)
    max_theoretical_score = (0.4 * 10.0) + (0.3 * 30.0) + (0.2 * 100.0) + (0.1 * 10.0) # 34.0
    emp_percentage = (raw_emp_score / max_theoretical_score) * 100
    
    # Creating three columns for key metrics
    col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
    
    # Preparing variables for the outcome card
    status_badge = "<span class='badge-placed'>PLACED</span>" if prediction_class == 1 else "<span class='badge-unplaced'>NOT PLACED</span>"
    status_desc = "Model predicts high likelihood of campus placement." if prediction_class == 1 else "Model predicts placement difficulty under current profile."
    
    # Rendering the Placement Outcome metric card
    col_metrics1.markdown(f"""
    <div class='metric-card'>
        <h4 style='margin: 0; color: #8b949e; font-size: 16px;'>Placement Outcome</h4>
        <h2 style='margin: 10px 0;'>{status_badge}</h2>
        <p style='margin: 0; font-size: 14px; color: #c9d1d9;'>{status_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rendering the Placement Probability metric card
    col_metrics2.markdown(f"""
    <div class='metric-card'>
        <h4 style='margin: 0; color: #8b949e; font-size: 16px;'>Placement Probability</h4>
        <h2 style='margin: 10px 0; color: #58a6ff; font-size: 32px; font-weight: bold;'>{prediction_prob * 100:.1f}%</h2>
        <p style='margin: 0; font-size: 14px; color: #c9d1d9;'>Confidence score generated by Random Forest classifier.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rendering the Employability Score metric card
    col_metrics3.markdown(f"""
    <div class='metric-card'>
        <h4 style='margin: 0; color: #8b949e; font-size: 16px;'>Employability Score</h4>
        <h2 style='margin: 10px 0; color: #bc8cff; font-size: 32px; font-weight: bold;'>{raw_emp_score:.2f} <span style='font-size: 14px; color: #8b949e; font-weight: normal;'>/ {max_theoretical_score} ({emp_percentage:.1f}%)</span></h2>
        <p style='margin: 0; font-size: 14px; color: #c9d1d9;'>Multi-dimensional score calculated from weighted skills and experience.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Extracting averages of placed students in the selected branch for comparison
    df_placed_branch = df_data[(df_data["Branch"] == input_branch) & (df_data["Placed"] == 1)]
    
    if len(df_placed_branch) > 0:
        avg_placed_cgpa = df_placed_branch["CGPA"].mean()
        avg_placed_coding = df_placed_branch["Coding_Skills"].mean()
        avg_placed_comm = df_placed_branch["Communication_Skills"].mean()
        avg_placed_soft = df_placed_branch["Soft_Skills_Rating"].mean()
        avg_placed_projects = df_placed_branch["Projects"].mean()
        avg_placed_internships = df_placed_branch["Internships"].mean()
        avg_placed_certifications = df_placed_branch["Certifications"].mean()
        avg_placed_aptitude = df_placed_branch["Aptitude_Test_Score"].mean()
    else:
        # Setting fallback values if no placed students exist in the database for the branch
        avg_placed_cgpa, avg_placed_coding, avg_placed_comm, avg_placed_soft, avg_placed_projects, avg_placed_internships, avg_placed_certifications, avg_placed_aptitude = 7.5, 6.0, 6.0, 6.0, 4.0, 1.0, 2.0, 75.0

    # Rendering dynamic, personalized recommendations directly below the outputs
    st.markdown("### 💡 Personalized Career Correction & Action Plan")
    st.write("Dynamic suggestions computed based on your inputs compared to successfully placed student benchmarks:")
    
    # Evaluating academic recommendations
    if input_backlogs > 0:
        st.markdown(f"""
        <div class='reco-box' style='border-color: #ff7b72;'>
            <strong>⚠️ Clear Active Backlogs:</strong> You currently have {input_backlogs} active backlog(s). 
            Most core and MNC recruiters filter out profiles with active backlogs during registration. 
            Prioritize clearing your backlogs to expand placement eligibility.
        </div>
        """, unsafe_allow_html=True)
        
    if input_cgpa < avg_placed_cgpa:
        st.markdown(f"""
        <div class='reco-box'>
            <strong>📈 Improve Academic Performance:</strong> Your CGPA of {input_cgpa:.2f} is below the average CGPA 
            of successfully placed students in {input_branch} ({avg_placed_cgpa:.2f}). Focus on scoring well in 
            the upcoming semesters to cross the typical placement cutoff of 7.5+ or 8.0+.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='reco-box' style='border-left-color: #3fb950;'>
            <strong>🌟 Strong Academics:</strong> Congratulations! Your CGPA of {input_cgpa:.2f} is above the average 
            of placed students ({avg_placed_cgpa:.2f}), making you eligible for high-tier company processes.
        </div>
        """, unsafe_allow_html=True)
        
    # Evaluating coding and technical skills recommendations
    if input_coding < avg_placed_coding:
        st.markdown(f"""
        <div class='reco-box'>
            <strong>💻 Boost Coding Skills:</strong> Placed students in your branch average a coding rating of {avg_placed_coding:.2f}/10, 
            while yours is entered as {input_coding}/10. Dedicate time to structured coding platforms (LeetCode, HackerRank, GeeksforGeeks) 
            to ace technical coding assessments.
        </div>
        """, unsafe_allow_html=True)
        
    if input_aptitude < avg_placed_aptitude:
        st.markdown(f"""
        <div class='reco-box'>
            <strong>🧮 Practice Quantitative Aptitude:</strong> Your aptitude test score of {input_aptitude} is below the average 
            of placed candidates ({avg_placed_aptitude:.1f}). Focus on practicing quantitative problems, logical reasoning, 
            and data interpretation tests, as these represent the primary screening round for most jobs.
        </div>
        """, unsafe_allow_html=True)
        
    # Evaluating experience recommendations
    if input_internships == 0:
        st.markdown("""
        <div class='reco-box'>
            <strong>💼 Pursue Internships:</strong> You have completed 0 internships. Having at least 1 internship 
            substantially improves your resume's strength and helps you explain industry-readiness in interviews. 
            Look out for summer internships or virtual research projects.
        </div>
        """, unsafe_allow_html=True)
        
    if input_projects < 2:
        st.markdown("""
        <div class='reco-box'>
            <strong>📁 Build Domain Projects:</strong> Undertake 2 to 3 hands-on practical projects in your field. 
            This allows you to demonstrate active problem-solving skills and provides talking points in technical rounds.
        </div>
        """, unsafe_allow_html=True)
        
    if input_certifications < 1:
        st.markdown("""
        <div class='reco-box'>
            <strong>📜 Earn Professional Certifications:</strong> Industry credentials (from AWS, Oracle, Google, Coursera, etc.) 
            validate your specialized expertise and show self-motivation. Plan to complete at least one certification soon.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Creating layout for charts and analysis
    col_plot1, col_plot2 = st.columns([1, 1])
        
    with col_plot1:
        st.markdown("### 📊 Skill Comparison Radar Chart")
        st.write(f"Comparing entered ratings against average of successfully **Placed** students in **{input_branch}**.")
        
        # Defining categories and values for radar chart
        radar_categories = ["Coding Skills", "Communication", "Soft Skills", "Projects", "Internships", "Certifications"]
        student_radar_vals = [input_coding, input_comm, input_soft, input_projects, input_internships * 2.5, input_certifications * 2.5] # scaled for radar
        placed_radar_vals = [avg_placed_coding, avg_placed_comm, avg_placed_soft, avg_placed_projects, avg_placed_internships * 2.5, avg_placed_certifications * 2.5]
        
        # Plotting the radar chart using Plotly graph objects
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=student_radar_vals,
            theta=radar_categories,
            fill='toself',
            name='Current Student',
            line_color='#bc8cff',
            fillcolor='rgba(188, 140, 255, 0.3)'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=placed_radar_vals,
            theta=radar_categories,
            fill='toself',
            name='Average Placed Student',
            line_color='#58a6ff',
            fillcolor='rgba(56, 139, 253, 0.2)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], color="#8b949e", gridcolor="#30363d"),
                angularaxis=dict(color="#8b949e", gridcolor="#30363d"),
                bgcolor="rgba(22, 27, 34, 0.5)"
            ),
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#c9d1d9")),
            margin=dict(t=30, b=30, l=30, r=30)
        )
        
        st.plotly_chart(fig_radar, width="stretch")
        
    with col_plot2:
        st.markdown("### ⏱️ Placement Probability Gauge")
        st.write("Visualizing prediction confidence and likelihood metric.")
        
        # Plotting the gauge chart using Plotly indicator
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction_prob * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'color': "#c9d1d9", 'size': 50}},
            title={'text': "Likelihood of Placement", 'font': {'color': "#8b949e", 'size': 18}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#8b949e"},
                'bar': {'color': "#58a6ff"},
                'bgcolor': "rgba(22, 27, 34, 0.5)",
                'borderwidth': 2,
                'bordercolor': "#30363d",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(248, 81, 73, 0.15)'},
                    {'range': [40, 75], 'color': 'rgba(219, 109, 40, 0.15)'},
                    {'range': [75, 100], 'color': 'rgba(46, 160, 67, 0.15)'}
                ],
                'threshold': {
                    'line': {'color': "#ff7b72", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=50, b=20, l=30, r=30),
            height=320
        )
        
        st.plotly_chart(fig_gauge, width="stretch")

with tab_batch:
    # Creating header for the batch upload prediction portal
    st.markdown("<h1 class='gradient-text'>Recruiter Portal & Batch Predictions</h1>", unsafe_allow_html=True)
    st.write("Upload a CSV file containing multiple student profiles to perform batch classifications and calculate employability scores instantly.")
    
    st.markdown("---")
    
    # Providing a template download option for recruiters
    st.markdown("### 📥 Download CSV Schema Template")
    st.write("Ensure your upload CSV follows the schema below. Click to download the template:")
    
    template_data = pd.DataFrame([{
        "Age": 21,
        "Gender": "Female",
        "Degree": "B.Tech",
        "Branch": "CSE",
        "CGPA": 8.5,
        "Internships": 2,
        "Projects": 4,
        "Coding_Skills": 8,
        "Communication_Skills": 7,
        "Aptitude_Test_Score": 85,
        "Soft_Skills_Rating": 7,
        "Certifications": 2,
        "Backlogs": 0
    }])
    
    # Rendering template csv download button
    template_csv = template_data.to_csv(index=False)
    st.download_button(
        label="Download Sample CSV Template",
        data=template_csv,
        file_name="student_schema_template.csv",
        mime="text/csv"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Rendering file uploader to receive batch inputs
    st.markdown("### 📤 Upload Student Dataset")
    uploaded_file = st.file_uploader("Select a student CSV file...", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Reading the uploaded file directly into a pandas dataframe
            df_upload = pd.read_csv(uploaded_file)
            
            st.success("File uploaded successfully! Processing records...")
            
            # Verifying required features exist in the file
            required_cols = ["Age", "Gender", "Degree", "Branch", "CGPA", "Internships", 
                             "Projects", "Coding_Skills", "Communication_Skills", 
                             "Aptitude_Test_Score", "Soft_Skills_Rating", "Certifications", "Backlogs"]
            
            missing_cols = [c for c in required_cols if c not in df_upload.columns]
            
            if len(missing_cols) > 0:
                st.error(f"Missing required columns in CSV: {missing_cols}")
            else:
                # Engineering feature columns for batch predictions
                df_upload["Avg_Skill_Score"] = (df_upload["Coding_Skills"] + df_upload["Communication_Skills"] + df_upload["Soft_Skills_Rating"]) / 3.0
                df_upload["Experience_Score"] = (df_upload["Internships"] * 2) + df_upload["Projects"] + df_upload["Certifications"]
                
                # Executing batch model predictions
                pred_features = df_upload[features]
                
                batch_preds = placement_model.predict(pred_features)
                batch_probs = placement_model.predict_proba(pred_features)[:, 1]
                
                # Calculating the Employability Score for each row using the SQL formula
                batch_emp = (0.4 * df_upload["Avg_Skill_Score"]) + (0.3 * df_upload["Experience_Score"]) + (0.2 * df_upload["Aptitude_Test_Score"]) + (0.1 * df_upload["Soft_Skills_Rating"])
                
                # Appending the calculations to the uploaded dataframe
                df_upload["Predicted_Placement"] = np.where(batch_preds == 1, "Placed", "Not Placed")
                df_upload["Placement_Probability (%)"] = np.round(batch_probs * 100, 2)
                df_upload["Employability_Score"] = np.round(batch_emp, 2)
                
                st.markdown("### 🔍 Batch Prediction Preview")
                st.write("Displaying first 10 processed student profiles:")
                
                # Formatting table with prediction results
                preview_cols = ["Degree", "Branch", "CGPA", "Backlogs", "Predicted_Placement", "Placement_Probability (%)", "Employability_Score"]
                st.dataframe(df_upload[preview_cols].head(10), width="stretch")
                
                # Plotting visual summary of batch prediction distributions
                st.markdown("### 📊 Batch Distributions Summary")
                
                col_sum1, col_sum2 = st.columns(2)
                
                with col_sum1:
                    # Rendering bar chart of predicted placement outcomes
                    fig_batch_bar = px.histogram(
                        df_upload, 
                        x="Predicted_Placement", 
                        color="Predicted_Placement", 
                        title="Distribution of Predicted Placements",
                        color_discrete_map={"Placed": "#3fb950", "Not Placed": "#ff7b72"},
                        labels={"Predicted_Placement": "Placement Prediction"}
                    )
                    fig_batch_bar.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#c9d1d9",
                        showlegend=False
                    )
                    st.plotly_chart(fig_batch_bar, width="stretch")
                    
                with col_sum2:
                    # Rendering box plot of employability scores by branch
                    fig_batch_box = px.box(
                        df_upload, 
                        x="Branch", 
                        y="Employability_Score", 
                        color="Predicted_Placement",
                        title="Employability Score by Branch & Predicted Outcome",
                        color_discrete_map={"Placed": "#3fb950", "Not Placed": "#ff7b72"}
                    )
                    fig_batch_box.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#c9d1d9"
                    )
                    st.plotly_chart(fig_batch_box, width="stretch")
                
                # Providing complete batch predictions download button
                result_csv = df_upload.to_csv(index=False)
                st.download_button(
                    label="Download Complete Prediction Report (CSV)",
                    data=result_csv,
                    file_name="student_placement_predictions_report.csv",
                    mime="text/csv"
                )
                
        except Exception as e:
            st.error(f"An error occurred while parsing the CSV file: {str(e)}")
