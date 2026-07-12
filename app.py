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
    /* Importing premium typography from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Styling the main container and backgrounds */
    .stApp {
        background: linear-gradient(135deg, #07090e 0%, #0f1423 50%, #080c16 100%);
        color: #e6edf3;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Styling headers and custom font styles */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Customizing sidebar layout and styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(48, 54, 61, 0.6) !important;
    }
    
    /* Styling the widgets and sliders */
    .stSlider [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Designing glassmorphic metric cards */
    .metric-card {
        background: rgba(15, 20, 35, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    /* Implementing lift and glow animations on card hover */
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(88, 166, 255, 0.6);
        box-shadow: 0 12px 40px rgba(56, 139, 253, 0.2);
    }
    
    /* Styling headers and custom color gradients */
    .gradient-text {
        background: linear-gradient(90deg, #58a6ff 0%, #bc8cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Designing placement status badges */
    .badge-placed {
        background: linear-gradient(135deg, rgba(46, 160, 67, 0.1) 0%, rgba(46, 160, 67, 0.25) 100%);
        color: #56ee73;
        border: 1px solid rgba(86, 238, 115, 0.4);
        text-shadow: 0 0 10px rgba(86, 238, 115, 0.25);
        padding: 6px 14px;
        border-radius: 30px;
        font-weight: 700;
        display: inline-block;
        font-size: 20px;
        letter-spacing: 0.5px;
    }
    
    .badge-unplaced {
        background: linear-gradient(135deg, rgba(248, 81, 73, 0.1) 0%, rgba(248, 81, 73, 0.25) 100%);
        color: #ff7b72;
        border: 1px solid rgba(248, 81, 73, 0.4);
        text-shadow: 0 0 10px rgba(248, 81, 73, 0.25);
        padding: 6px 14px;
        border-radius: 30px;
        font-weight: 700;
        display: inline-block;
        font-size: 20px;
        letter-spacing: 0.5px;
    }
    
    /* Designing personalized recommendation boxes with icons */
    .reco-box-warning {
        background: rgba(248, 81, 73, 0.03);
        border: 1px solid rgba(248, 81, 73, 0.2);
        border-left: 5px solid #ff7b72;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    
    .reco-box-info {
        background: rgba(56, 139, 253, 0.03);
        border: 1px solid rgba(56, 139, 253, 0.2);
        border-left: 5px solid #58a6ff;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    
    .reco-box-success {
        background: rgba(46, 160, 67, 0.03);
        border: 1px solid rgba(46, 160, 67, 0.2);
        border-left: 5px solid #3fb950;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    
    /* Styling Streamlit UI elements like tabs and buttons */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 20, 35, 0.3);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(48, 54, 61, 0.4);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre;
        background-color: transparent;
        border-radius: 6px;
        color: #8b949e;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        padding: 0px 16px;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(56, 139, 253, 0.15) !important;
        color: #58a6ff !important;
        font-weight: 600 !important;
    }
    
    /* Customizing file uploader and buttons */
    .stButton>button {
        background: linear-gradient(135deg, #1f6feb 0%, #0948b3 100%) !important;
        border: none !important;
        color: white !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4);
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
st.sidebar.markdown("<h2 class='gradient-text' style='font-size: 26px; margin-bottom: 5px;'>Profile Configurator</h2>", unsafe_allow_html=True)
st.sidebar.write("Adjust the parameters to simulate placement evaluations.")

# Designing sidebar sections with expanders to declutter inputs and improve user experience
with st.sidebar.expander("👤 Personal Details", expanded=True):
    input_age = st.slider("Age", min_value=18, max_value=24, value=21, step=1, help="The current age of the candidate.")
    input_gender = st.selectbox("Gender", options=["Female", "Male"], help="Biological gender classification.")

with st.sidebar.expander("🎓 Academic Profile", expanded=True):
    input_degree = st.selectbox("Degree Type", options=sorted(df_data["Degree"].unique()), help="Enrolled degree program.")
    input_branch = st.selectbox("Branch / Specialization", options=sorted(df_data["Branch"].unique()), help="Academic stream branch.")
    input_cgpa = st.slider("Cumulative GPA (CGPA)", min_value=1.0, max_value=10.0, value=7.2, step=0.1, help="Current cumulative academic GPA.")
    input_backlogs = st.slider("Active/History Backlogs", min_value=0, max_value=5, value=0, step=1, help="Count of accumulated uncleared courses.")

with st.sidebar.expander("🛠️ Practical Experience", expanded=True):
    input_internships = st.slider("Number of Internships", min_value=0, max_value=5, value=1, step=1, help="Total internships completed.")
    input_projects = st.slider("Number of Projects Done", min_value=0, max_value=10, value=3, step=1, help="Hands-on domain projects completed.")
    input_certifications = st.slider("Certifications Completed", min_value=0, max_value=10, value=2, step=1, help="Industry-recognized certifications earned.")

with st.sidebar.expander("🧠 Skills & Ratings", expanded=True):
    input_coding = st.slider("Coding Skills Rating", min_value=1, max_value=10, value=6, step=1, help="Technical programming competency.")
    input_comm = st.slider("Communication Skills Rating", min_value=1, max_value=10, value=6, step=1, help="Verbal and written communication rating.")
    input_aptitude = st.slider("Aptitude Test Score", min_value=0, max_value=100, value=70, step=5, help="Quantitative reasoning score.")
    input_soft = st.slider("Soft Skills Rating", min_value=1, max_value=10, value=6, step=1, help="Interpersonal and teamwork competency rating.")

# Displaying main dashboard tabs
tab_individual, tab_batch = st.tabs(["🎯 Placement Predictor & Profiler", "📊 Recruiters Portal & Batch Prediction"])

with tab_individual:
    # Creating header for the individual prediction tab
    st.markdown("<h1 class='gradient-text' style='margin-bottom: 2px;'>Student Placement Intelligence</h1>", unsafe_allow_html=True)
    st.write("An advanced predictive analytics platform leveraging machine learning to model student employability outcomes.")
    st.markdown("<hr style='border-top: 1px solid rgba(48, 54, 61, 0.4); margin: 15px 0;'>", unsafe_allow_html=True)
    
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
    raw_emp_score = (0.4 * avg_skill) + (0.3 * exp_score) + (0.2 * input_aptitude) + (0.1 * input_soft)
    max_theoretical_score = (0.4 * 10.0) + (0.3 * 30.0) + (0.2 * 100.0) + (0.1 * 10.0) # 34.0
    emp_percentage = (raw_emp_score / max_theoretical_score) * 100
    
    # Creating three columns for key metrics
    col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
    
    # Preparing variables for the outcome card
    status_badge = "<span class='badge-placed'>PLACED</span>" if prediction_class == 1 else "<span class='badge-unplaced'>NOT PLACED</span>"
    status_desc = "Model predicts a high likelihood of campus placement success." if prediction_class == 1 else "Model predicts placement challenges under the current profile."
    
    # Rendering the Placement Outcome metric card with SVG icons
    col_metrics1.markdown(f"""
    <div class='metric-card'>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
            <div style='background: rgba(46, 160, 67, 0.15); padding: 8px; border-radius: 8px; display: flex;'>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3fb950" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/></svg>
            </div>
            <h4 style='margin: 0; color: #8b949e; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Placement Outcome</h4>
        </div>
        <h2 style='margin: 10px 0;'>{status_badge}</h2>
        <p style='margin: 0; font-size: 13px; color: #8b949e; line-height: 1.4;'>{status_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rendering the Placement Probability metric card with SVG icons
    col_metrics2.markdown(f"""
    <div class='metric-card'>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
            <div style='background: rgba(56, 139, 253, 0.15); padding: 8px; border-radius: 8px; display: flex;'>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </div>
            <h4 style='margin: 0; color: #8b949e; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Placement Probability</h4>
        </div>
        <h2 style='margin: 10px 0; color: #58a6ff; font-size: 32px; font-weight: 800; font-family: "Space Grotesk", sans-serif;'>{prediction_prob * 100:.1f}%</h2>
        <p style='margin: 0; font-size: 13px; color: #8b949e; line-height: 1.4;'>Calibrated classifier estimation likelihood.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rendering the Employability Score metric card with SVG icons
    col_metrics3.markdown(f"""
    <div class='metric-card'>
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
            <div style='background: rgba(188, 140, 255, 0.15); padding: 8px; border-radius: 8px; display: flex;'>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bc8cff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>
            </div>
            <h4 style='margin: 0; color: #8b949e; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Employability Index</h4>
        </div>
        <h2 style='margin: 10px 0; color: #bc8cff; font-size: 32px; font-weight: 800; font-family: "Space Grotesk", sans-serif;'>{raw_emp_score:.2f} <span style='font-size: 14px; color: #8b949e; font-weight: 400;'>/ {max_theoretical_score} ({emp_percentage:.1f}%)</span></h2>
        <p style='margin: 0; font-size: 13px; color: #8b949e; line-height: 1.4;'>Multi-dimensional index mapped from weighted stats.</p>
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
    st.write("Dynamic actions computed based on your profile inputs compared to branch placement benchmarks:")
    
    # Evaluating academic recommendations
    if input_backlogs > 0:
        st.markdown(f"""
        <div class='reco-box-warning'>
            <div style='background: rgba(248, 81, 73, 0.15); padding: 6px; border-radius: 6px; display: flex;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff7b72" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            </div>
            <div>
                <strong style='color: #ff7b72; font-size: 15px; display: block; margin-bottom: 4px;'>Clear Active Backlogs</strong>
                <span style='font-size: 13px; color: #c9d1d9;'>You currently have {input_backlogs} active backlog(s). Most core and MNC recruiters filter out profiles with active backlogs during registration. Prioritize clearing your backlogs to expand placement eligibility.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    if input_cgpa < avg_placed_cgpa:
        st.markdown(f"""
        <div class='reco-box-info'>
            <div style='background: rgba(56, 139, 253, 0.15); padding: 6px; border-radius: 6px; display: flex;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            </div>
            <div>
                <strong style='color: #58a6ff; font-size: 15px; display: block; margin-bottom: 4px;'>Improve Academic Performance</strong>
                <span style='font-size: 13px; color: #c9d1d9;'>Your CGPA of {input_cgpa:.2f} is below the average CGPA of successfully placed students in {input_branch} ({avg_placed_cgpa:.2f}). Focus on scoring well in the upcoming semesters to cross the typical placement cutoff of 7.5+ or 8.0+.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='reco-box-success'>
            <div style='background: rgba(46, 160, 67, 0.15); padding: 6px; border-radius: 6px; display: flex;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3fb950" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            </div>
            <div>
                <strong style='color: #3fb950; font-size: 15px; display: block; margin-bottom: 4px;'>Strong Academic Standing</strong>
                <span style='font-size: 13px; color: #c9d1d9;'>Congratulations! Your CGPA of {input_cgpa:.2f} is above the average of placed students ({avg_placed_cgpa:.2f}), making you eligible for high-tier company processes.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Evaluating coding and technical skills recommendations
    if input_coding < avg_placed_coding:
        st.markdown(f"""
        <div class='reco-box-info'>
            <div style='background: rgba(56, 139, 253, 0.15); padding: 6px; border-radius: 6px; display: flex;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            </div>
            <div>
                <strong style='color: #58a6ff; font-size: 15px; display: block; margin-bottom: 4px;'>Boost Coding Skills</strong>
                <span style='font-size: 13px; color: #c9d1d9;'>Placed students in your branch average a coding rating of {avg_placed_coding:.2f}/10, while yours is entered as {input_coding}/10. Dedicate time to structured coding platforms (LeetCode, HackerRank, GeeksforGeeks) to ace technical coding assessments.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    if input_aptitude < avg_placed_aptitude:
        st.markdown(f"""
        <div class='reco-box-info'>
            <div style='background: rgba(56, 139, 253, 0.15); padding: 6px; border-radius: 6px; display: flex;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            </div>
            <div>
                <strong style='color: #58a6ff; font-size: 15px; display: block; margin-bottom: 4px;'>Practice Quantitative Aptitude</strong>
                <span style='font-size: 13px; color: #c9d1d9;'>Your aptitude test score of {input_aptitude} is below the average of placed candidates ({avg_placed_aptitude:.1f}). Focus on practicing quantitative problems, logical reasoning, and data interpretation tests, as these represent the primary screening round for most jobs.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Evaluating experience recommendations
    if input_internships == 0:
        st.markdown("""
        <div class='reco-box-info'>
            <div style='background: rgba(56, 139, 253, 0.15); padding: 6px; border-radius: 6px; display: flex;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            </div>
            <div>
                <strong style='color: #58a6ff; font-size: 15px; display: block; margin-bottom: 4px;'>Pursue Internships</strong>
                <span style='font-size: 13px; color: #c9d1d9;'>You have completed 0 internships. Having at least 1 internship substantially improves your resume's strength and helps you explain industry-readiness in interviews. Look out for summer internships or virtual research projects.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    if input_projects < 2:
        st.markdown("""
        <div class='reco-box-info'>
            <div style='background: rgba(56, 139, 253, 0.15); padding: 6px; border-radius: 6px; display: flex;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
            </div>
            <div>
                <strong style='color: #58a6ff; font-size: 15px; display: block; margin-bottom: 4px;'>Build Domain Projects</strong>
                <span style='font-size: 13px; color: #c9d1d9;'>Undertake 2 to 3 hands-on practical projects in your field. This allows you to demonstrate active problem-solving skills and provides talking points in technical rounds.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    if input_certifications < 1:
        st.markdown("""
        <div class='reco-box-info'>
            <div style='background: rgba(56, 139, 253, 0.15); padding: 6px; border-radius: 6px; display: flex;'>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div>
                <strong style='color: #58a6ff; font-size: 15px; display: block; margin-bottom: 4px;'>Earn Professional Certifications</strong>
                <span style='font-size: 13px; color: #c9d1d9;'>Industry credentials validate your specialized expertise and show self-motivation. Plan to complete at least one certification soon.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 1px solid rgba(48, 54, 61, 0.4); margin: 15px 0;'>", unsafe_allow_html=True)
    
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
            fillcolor='rgba(188, 140, 255, 0.25)'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=placed_radar_vals,
            theta=radar_categories,
            fill='toself',
            name='Average Placed Student',
            line_color='#58a6ff',
            fillcolor='rgba(56, 139, 253, 0.15)'
        ))
        
        # Updating layout of radar chart for premium styling
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10], 
                    color="#8b949e", 
                    gridcolor="rgba(48, 54, 61, 0.4)",
                    linecolor="rgba(48, 54, 61, 0.4)",
                    tickfont=dict(family="Plus Jakarta Sans", size=10)
                ),
                angularaxis=dict(
                    color="#c9d1d9", 
                    gridcolor="rgba(48, 54, 61, 0.4)",
                    tickfont=dict(family="Space Grotesk", size=12)
                ),
                bgcolor="rgba(15, 20, 35, 0.3)"
            ),
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                font=dict(family="Plus Jakarta Sans", color="#c9d1d9", size=11),
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=20, b=40, l=40, r=40)
        )
        
        st.plotly_chart(fig_radar, width="stretch")
        
    with col_plot2:
        st.markdown("### ⏱️ Placement Probability Gauge")
        st.write("Visualizing prediction confidence and likelihood metric.")
        
        # Defining dynamic color for the gauge bar depending on probability thresholds
        gauge_bar_color = "#3fb950" if prediction_prob >= 0.75 else ("#db6d28" if prediction_prob >= 0.4 else "#ff7b72")
        
        # Plotting the gauge chart using Plotly indicator
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction_prob * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'color': "#e6edf3", 'size': 50, 'family': "Space Grotesk"}},
            title={'text': "Likelihood of Placement", 'font': {'color': "#8b949e", 'size': 16, 'family': "Plus Jakarta Sans"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#8b949e"},
                'bar': {'color': gauge_bar_color},
                'bgcolor': "rgba(15, 20, 35, 0.3)",
                'borderwidth': 1.5,
                'bordercolor': "rgba(48, 54, 61, 0.4)",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(248, 81, 73, 0.08)'},
                    {'range': [40, 75], 'color': 'rgba(219, 109, 40, 0.08)'},
                    {'range': [75, 100], 'color': 'rgba(46, 160, 67, 0.08)'}
                ],
                'threshold': {
                    'line': {'color': "#58a6ff", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        
        # Updating layout of gauge chart for premium styling
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=50, b=10, l=30, r=30),
            height=280
        )
        
        st.plotly_chart(fig_gauge, width="stretch")

with tab_batch:
    # Creating header for the batch upload prediction portal
    st.markdown("<h1 class='gradient-text' style='margin-bottom: 2px;'>Recruiter Portal & Batch Predictions</h1>", unsafe_allow_html=True)
    st.write("Upload a CSV file containing multiple student profiles to perform batch classifications and calculate employability scores instantly.")
    st.markdown("<hr style='border-top: 1px solid rgba(48, 54, 61, 0.4); margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Ingesting subcomponents into visual columns to clean template download area
    col_temp1, col_temp2 = st.columns([2, 1])
    with col_temp1:
        st.markdown("### 📥 Download CSV Schema Template")
        st.write("Ensure your upload CSV follows the schema. Download the official CSV template below:")
    
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
    with col_temp2:
        st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
        st.download_button(
            label="Download Template CSV",
            data=template_csv,
            file_name="student_schema_template.csv",
            mime="text/csv"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Rendering file uploader to receive batch inputs
    st.markdown("### 📤 Upload Student Dataset")
    uploaded_file = st.file_uploader("Select a student CSV file to process...", type=["csv"])
    
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
                
                # Defining list of features to match training schema
                features = ["Age", "Gender", "Degree", "Branch", "CGPA", "Internships", "Projects", 
                            "Coding_Skills", "Communication_Skills", "Aptitude_Test_Score", 
                            "Soft_Skills_Rating", "Certifications", "Backlogs", "Avg_Skill_Score", "Experience_Score"]
                
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
                    # Styling the chart layout for premium dark-theme integration
                    fig_batch_bar.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#e6edf3",
                        font_family="Plus Jakarta Sans",
                        title_font_family="Space Grotesk",
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
                    # Styling the chart layout for premium dark-theme integration
                    fig_batch_box.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="#e6edf3",
                        font_family="Plus Jakarta Sans",
                        title_font_family="Space Grotesk"
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
