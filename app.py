import os
import streamlit as st
import pandas as pd
import numpy as np
import time
from pipeline.prediction_pipeline import PredictionPipeline

# Page configuration
st.set_page_config(
    page_title="AI Student Impact Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #a8b2d1;
        margin-bottom: 2rem;
    }
    
    .result-card {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1) 0%, rgba(79, 172, 254, 0.1) 100%);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-top: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .gpa-score {
        font-size: 3.5rem;
        font-weight: 800;
        color: #00ff88;
        margin: 0.5rem 0;
    }
    
    .custom-footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: #8892b0;
        font-size: 0.95rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .custom-footer a {
        color: #00f2fe;
        text-decoration: none;
        font-weight: bold;
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000;
        font-size: 1.15rem;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 2rem;
        width: 100%;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 201, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<div class='main-title'>AI Student Impact Predictor 🎓</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Predict post-semester GPA based on Generative AI tool usage and study habits</div>", unsafe_allow_html=True)

# Safe Pipeline Loader
@st.cache_resource
def get_prediction_pipeline():
    try:
        return PredictionPipeline(), True
    except Exception:
        return None, False

pipeline, pipeline_ready = get_prediction_pipeline()

# Input Form
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📚 Academic Profile")
        major = st.selectbox(
            "Major Category",
            options=["Humanities", "Medical", "Business", "Engineering", "Science", "Arts"],
            index=0
        )
        year = st.selectbox(
            "Year of Study",
            options=["Freshman", "Sophomore", "Junior", "Senior"],
            index=2
        )
        pre_gpa = st.slider(
            "Pre-Semester GPA",
            min_value=0.0,
            max_value=4.0,
            value=3.0,
            step=0.01,
            help="Your cumulative GPA prior to this semester."
        )
        traditional_study = st.slider(
            "Traditional Study Hours / Week",
            min_value=0.0,
            max_value=40.0,
            value=15.0,
            step=0.5
        )

    with col2:
        st.markdown("### 🤖 AI Tool Usage")
        genai_hours = st.slider(
            "Weekly GenAI Usage (Hours)",
            min_value=0.0,
            max_value=40.0,
            value=10.0,
            step=0.5
        )
        use_case = st.selectbox(
            "Primary Use Case",
            options=["Copywriting/Drafting", "Ideation", "Summarizing_Reading", "Coding/Debugging", "Math/Data_Analysis"],
            index=1
        )
        prompt_skill = st.select_slider(
            "Prompt Engineering Skill",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate"
        )
        tool_diversity = st.number_input(
            "Tool Diversity (Number of AI Tools)",
            min_value=1,
            max_value=10,
            value=2
        )
        has_paid_sub = st.checkbox("Has Paid AI Subscription (e.g. ChatGPT Plus)", value=False)

    with col3:
        st.markdown("### 🧠 Habits & Psychology")
        ai_dependency = st.slider(
            "Perceived AI Dependency (1-5)",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Minimal dependency, 5 = Heavily reliant on AI"
        )
        exam_anxiety = st.slider(
            "Exam Anxiety Level (1-10)",
            min_value=1,
            max_value=10,
            value=5
        )
        skill_retention = st.slider(
            "Skill Retention Score (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=0.5
        )
        burnout = st.select_slider(
            "Burnout Risk Level",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        policy = st.selectbox(
            "Institutional Policy on AI",
            options=["Allowed_With_Citation", "Strict_Ban", "Unrestricted", "No_Clear_Policy"],
            index=0
        )

# Predict Button
st.write("")
predict_button = st.button("🔮 Predict Post-Semester GPA")

if predict_button:
    with st.spinner("Analyzing habits and calculating prediction..."):
        time.sleep(0.8)  # Smooth transition feel
        
        # Calculation logic
        if pipeline_ready and pipeline is not None:
            try:
                input_df = pd.DataFrame([{
                    "Major_Category": major,
                    "Year_of_Study": year,
                    "Pre_Semester_GPA": pre_gpa,
                    "Weekly_GenAI_Hours": genai_hours,
                    "Primary_Use_Case": use_case,
                    "Prompt_Engineering_Skill": prompt_skill,
                    "Tool_Diversity": tool_diversity,
                    "Has_Paid_Subscription": 1 if has_paid_sub else 0,
                    "Traditional_Study_Hours": traditional_study,
                    "Perceived_AI_Dependency": ai_dependency,
                    "Institutional_Policy": policy,
                    "Exam_Anxiety_Level": exam_anxiety,
                    "Skill_Retention_Score": skill_retention,
                    "Burnout_Risk_Level": burnout
                }])
                pred = pipeline.predict(input_df)[0][0]
                pred_gpa = min(max(float(pred), 0.0), 4.0)
                is_simulated = False
            except Exception:
                # Fallback calculation
                pred_gpa = round((pre_gpa * 0.7) + (traditional_study * 0.02) - (ai_dependency * 0.05) + (skill_retention * 0.01), 2)
                pred_gpa = min(max(pred_gpa, 0.0), 4.0)
                is_simulated = True
        else:
            pred_gpa = round((pre_gpa * 0.7) + (traditional_study * 0.02) - (ai_dependency * 0.05) + (skill_retention * 0.01), 2)
            pred_gpa = min(max(pred_gpa, 0.0), 4.0)
            is_simulated = True
        
        # Display Result
        st.markdown(f"""
        <div class='result-card'>
            <h3 style='margin:0; color:#cbd5e1;'>Predicted Post-Semester GPA</h3>
            <div class='gpa-score'>{pred_gpa:.2f}</div>
            <p style='color:#94a3b8; margin:0;'>Scale of 0.00 to 4.00</p>
        </div>
        """, unsafe_allow_html=True)
        
        if is_simulated:
            st.info("💡 *Note: Running in fast inference / simulated heuristic mode.*")

# Footer
st.markdown("""
<div class='custom-footer'>
    Impact of AI on Students • Developed with ❤️ by <a href='https://www.linkedin.com/in/tamimystic/' target='_blank'>tamimystic</a>
</div>
""", unsafe_allow_html=True)
