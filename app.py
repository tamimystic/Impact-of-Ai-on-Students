import os
import time
import streamlit as st
import pandas as pd
from pipeline.prediction_pipeline import PredictionPipeline

st.set_page_config(
    page_title="AI Student Impact Predictor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 1300px;
    }
    
    .header-box {
        text-align: center;
        margin-bottom: 1.2rem;
    }
    
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #f8fafc;
        margin: 0;
    }
    
    .sub-title {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }
    
    .section-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #38bdf8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.3rem;
    }
    
    .result-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        margin-top: 1rem;
    }
    
    .result-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94a3b8;
        margin-bottom: 0.4rem;
    }
    
    .result-value {
        font-size: 2.8rem;
        font-weight: 800;
        color: #38bdf8;
        line-height: 1;
        margin: 0.3rem 0;
    }
    
    .result-sub {
        font-size: 0.8rem;
        color: #64748b;
    }
    
    div.stButton > button {
        background: #0284c7;
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        width: 100%;
        transition: background 0.2s ease;
    }
    
    div.stButton > button:hover {
        background: #0369a1;
        color: #ffffff;
    }
    
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 1.5rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    .footer a {
        color: #38bdf8;
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    div[data-testid="stSlider"] {
        margin-bottom: -0.4rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='header-box'>
    <h1 class='main-title'>AI Student Impact Predictor</h1>
    <div class='sub-title'>Predict post-semester GPA based on Generative AI usage and study habits</div>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_prediction_pipeline():
    try:
        return PredictionPipeline(), True
    except Exception:
        return None, False

pipeline, pipeline_ready = get_prediction_pipeline()

left_col, mid_col, right_col = st.columns([1.1, 1.1, 1.0], gap="medium")

with left_col:
    st.markdown("<div class='section-title'>Academic & Study Profile</div>", unsafe_allow_html=True)
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
        value=3.20,
        step=0.01
    )
    traditional_study = st.slider(
        "Traditional Study Hours / Week",
        min_value=0.0,
        max_value=40.0,
        value=14.0,
        step=0.5
    )
    inst_policy = st.selectbox(
        "Institutional AI Policy",
        options=["Allowed_With_Citation", "Strict_Ban", "Unrestricted", "No_Clear_Policy"],
        index=0
    )

with mid_col:
    st.markdown("<div class='section-title'>AI Usage & Psychology</div>", unsafe_allow_html=True)
    genai_hours = st.slider(
        "Weekly GenAI Usage (Hours)",
        min_value=0.0,
        max_value=40.0,
        value=8.0,
        step=0.5
    )
    use_case = st.selectbox(
        "Primary Use Case",
        options=["Copywriting/Drafting", "Ideation", "Summarizing_Reading", "Coding/Debugging", "Math/Data_Analysis"],
        index=1
    )
    prompt_skill = st.select_slider(
        "Prompt Skill Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate"
    )
    ai_dependency = st.slider(
        "Perceived AI Dependency (1-5)",
        min_value=1,
        max_value=5,
        value=3
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
    tool_diversity = 2
    has_paid_sub = False

with right_col:
    st.markdown("<div class='section-title'>Prediction Panel</div>", unsafe_allow_html=True)
    st.write("")
    predict_clicked = st.button("Predict GPA")
    
    pred_gpa = None
    
    if predict_clicked:
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
                    "Institutional_Policy": inst_policy,
                    "Exam_Anxiety_Level": exam_anxiety,
                    "Skill_Retention_Score": skill_retention,
                    "Burnout_Risk_Level": burnout
                }])
                pred = pipeline.predict(input_df)[0][0]
                pred_gpa = min(max(float(pred), 0.0), 4.0)
            except Exception:
                calc = (pre_gpa * 0.70) + (traditional_study * 0.02) - (ai_dependency * 0.04) + (skill_retention * 0.008)
                pred_gpa = min(max(round(calc, 2), 0.0), 4.0)
        else:
            calc = (pre_gpa * 0.70) + (traditional_study * 0.02) - (ai_dependency * 0.04) + (skill_retention * 0.008)
            pred_gpa = min(max(round(calc, 2), 0.0), 4.0)
    else:
        calc = (pre_gpa * 0.70) + (traditional_study * 0.02) - (ai_dependency * 0.04) + (skill_retention * 0.008)
        pred_gpa = min(max(round(calc, 2), 0.0), 4.0)
    
    st.markdown(f"""
    <div class='result-container'>
        <div class='result-label'>Predicted Post-Semester GPA</div>
        <div class='result-value'>{pred_gpa:.2f}</div>
        <div class='result-sub'>Scale: 0.00 - 4.00</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    Impact of AI on Students • Developed by <a href='https://tamimystic.vercel.app/' target='_blank'>tamimystic</a>
</div>
""", unsafe_allow_html=True)
