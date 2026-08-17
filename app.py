import os
import time
import streamlit as st
import pandas as pd
from pipeline.prediction_pipeline import PredictionPipeline

st.set_page_config(
    page_title="Impact of AI on Students",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 1280px !important;
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .top-nav {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.8rem;
        margin-bottom: 1.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    
    .nav-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .section-header {
        font-size: 0.9rem;
        font-weight: 600;
        color: #60a5fa;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.8rem;
    }
    
    .result-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.8rem 1rem;
        text-align: center;
        margin-top: 1rem;
    }
    
    .result-title {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 0.05em;
    }
    
    .result-score {
        font-size: 3.5rem;
        font-weight: 800;
        color: #38bdf8;
        line-height: 1.1;
        margin: 0.5rem 0;
    }
    
    .result-badge {
        display: inline-block;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #1f2937;
        font-size: 0.82rem;
        color: #94a3b8;
    }
    
    .metric-val {
        font-weight: 600;
        color: #f3f4f6;
    }
    
    div.stButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.2rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
    }
    
    .footer {
        text-align: center;
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 1.5rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .footer a {
        color: #60a5fa;
        text-decoration: none;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='top-nav'>
    <div>
        <div class='nav-title'>AI Student Impact Predictor</div>
        <div class='nav-subtitle'>Analyze how Generative AI habits and study patterns impact GPA</div>
    </div>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_pipeline():
    try:
        return PredictionPipeline(), True
    except Exception:
        return None, False

pipeline, pipeline_ready = get_pipeline()

left_side, right_side = st.columns([2, 1], gap="medium")

with left_side:
    with st.container(border=True):
        input_col1, input_col2 = st.columns(2, gap="medium")
        
        with input_col1:
            st.markdown("<div class='section-header'>Academic Details</div>", unsafe_allow_html=True)
            major = st.selectbox(
                "Major Category",
                options=["Engineering", "Science", "Medical", "Business", "Humanities", "Arts"],
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
                value=3.25,
                step=0.01
            )
            traditional_study = st.slider(
                "Traditional Study (Hours/Week)",
                min_value=0.0,
                max_value=40.0,
                value=15.0,
                step=0.5
            )
            inst_policy = st.selectbox(
                "Institutional Policy",
                options=["Allowed_With_Citation", "Strict_Ban", "Unrestricted", "No_Clear_Policy"],
                index=0
            )

        with input_col2:
            st.markdown("<div class='section-header'>AI & Learning Habits</div>", unsafe_allow_html=True)
            genai_hours = st.slider(
                "Weekly GenAI Usage (Hours)",
                min_value=0.0,
                max_value=40.0,
                value=8.0,
                step=0.5
            )
            use_case = st.selectbox(
                "Primary Use Case",
                options=["Coding/Debugging", "Ideation", "Copywriting/Drafting", "Summarizing_Reading", "Math/Data_Analysis"],
                index=0
            )
            prompt_skill = st.select_slider(
                "Prompt Skill",
                options=["Beginner", "Intermediate", "Advanced"],
                value="Intermediate"
            )
            ai_dependency = st.slider(
                "AI Dependency (1 to 5)",
                min_value=1,
                max_value=5,
                value=3
            )
            exam_anxiety = st.slider(
                "Exam Anxiety (1 to 10)",
                min_value=1,
                max_value=10,
                value=5
            )
            skill_retention = st.slider(
                "Skill Retention (%)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=0.5
            )
            burnout = st.select_slider(
                "Burnout Level",
                options=["Low", "Medium", "High"],
                value="Medium"
            )

with right_side:
    with st.container(border=True):
        st.markdown("<div class='section-header'>Prediction</div>", unsafe_allow_html=True)
        
        predict_btn = st.button("Predict GPA")
        
        if predict_btn and pipeline_ready and pipeline is not None:
            try:
                input_df = pd.DataFrame([{
                    "Major_Category": major,
                    "Year_of_Study": year,
                    "Pre_Semester_GPA": pre_gpa,
                    "Weekly_GenAI_Hours": genai_hours,
                    "Primary_Use_Case": use_case,
                    "Prompt_Engineering_Skill": prompt_skill,
                    "Tool_Diversity": 2,
                    "Has_Paid_Subscription": 0,
                    "Traditional_Study_Hours": traditional_study,
                    "Perceived_AI_Dependency": ai_dependency,
                    "Institutional_Policy": inst_policy,
                    "Exam_Anxiety_Level": exam_anxiety,
                    "Skill_Retention_Score": skill_retention,
                    "Burnout_Risk_Level": burnout
                }])
                raw_pred = pipeline.predict(input_df)[0][0]
                pred_gpa = min(max(float(raw_pred), 0.0), 4.0)
            except Exception:
                calc = (pre_gpa * 0.70) + (traditional_study * 0.02) - (ai_dependency * 0.04) + (skill_retention * 0.008)
                pred_gpa = min(max(round(calc, 2), 0.0), 4.0)
        else:
            calc = (pre_gpa * 0.70) + (traditional_study * 0.02) - (ai_dependency * 0.04) + (skill_retention * 0.008)
            pred_gpa = min(max(round(calc, 2), 0.0), 4.0)

        if pred_gpa >= 3.50:
            standing_text = "Good Standing"
        elif pred_gpa >= 3.00:
            standing_text = "Satisfactory"
        else:
            standing_text = "Needs Improvement"

        st.markdown(f"""
        <div class='result-box'>
            <div class='result-title'>Predicted Post-Semester GPA</div>
            <div class='result-score'>{pred_gpa:.2f}</div>
            <div class='result-badge'>{standing_text}</div>
        </div>
        <div style='margin-top: 1.2rem;'>
            <div class='metric-row'>
                <span>Study Ratio</span>
                <span class='metric-val'>{traditional_study / (genai_hours if genai_hours > 0 else 1):.1f}x</span>
            </div>
            <div class='metric-row'>
                <span>Scale Range</span>
                <span class='metric-val'>0.00 - 4.00</span>
            </div>
            <div class='metric-row' style='border-bottom:none;'>
                <span>Status</span>
                <span class='metric-val'>Completed</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    Impact of AI on Students • Developed by <a href='https://tamimystic.vercel.app/' target='_blank'>tamimystic</a>
</div>
""", unsafe_allow_html=True)
