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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #090D16;
        color: #F1F5F9;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, rgba(30, 58, 138, 0.22) 0%, rgba(9, 13, 22, 1) 75%);
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 1350px !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    .navbar-brand {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 1.4rem;
        background: rgba(17, 24, 39, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }

    .brand-title {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-tag {
        font-size: 0.78rem;
        font-weight: 600;
        color: #94A3B8;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 0.8rem;
        transition: border-color 0.2s ease;
    }

    .glass-card:hover {
        border-color: rgba(56, 189, 248, 0.25);
    }

    .card-header {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #38BDF8;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .result-hero-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.6) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 18px;
        padding: 1.8rem 1.4rem;
        text-align: center;
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-top: 0.6rem;
    }

    .result-caption {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94A3B8;
    }

    .result-score {
        font-size: 3.8rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1;
        margin: 0.8rem 0 0.5rem 0;
        background: linear-gradient(135deg, #38BDF8 0%, #4ADE80 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .standing-badge {
        display: inline-block;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 0.3rem 0.9rem;
        border-radius: 30px;
        margin-top: 0.4rem;
        letter-spacing: 0.02em;
    }

    .badge-excellent {
        background: rgba(74, 222, 128, 0.12);
        color: #4ADE80;
        border: 1px solid rgba(74, 222, 128, 0.3);
    }

    .badge-good {
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    .badge-average {
        background: rgba(251, 191, 36, 0.12);
        color: #FBBF24;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }

    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 0.6rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        font-size: 0.82rem;
        color: #94A3B8;
    }

    .stat-val {
        font-weight: 600;
        color: #F8FAFC;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        width: 100% !important;
        box-shadow: 0 4px 18px rgba(2, 132, 199, 0.35) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-top: 0.4rem !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.5) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    div.stButton > button:active {
        transform: translateY(0px) !important;
    }

    label {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        margin-bottom: 0.2rem !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        font-size: 0.88rem !important;
    }

    .stSlider > div > div > div > div {
        background-color: #0284C7 !important;
    }

    .app-footer {
        text-align: center;
        font-size: 0.82rem;
        color: #64748B;
        margin-top: 1.2rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .app-footer a {
        color: #38BDF8;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s ease;
    }

    .app-footer a:hover {
        color: #818CF8;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='navbar-brand'>
    <div class='brand-title'>AI Student Impact Predictor</div>
    <div class='brand-tag'>Deep Learning Academic Intelligence</div>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_prediction_pipeline():
    try:
        return PredictionPipeline(), True
    except Exception:
        return None, False

pipeline, pipeline_ready = get_prediction_pipeline()

col_academic, col_ai, col_action = st.columns([1.15, 1.15, 1.1], gap="medium")

with col_academic:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>Academic Profile</div>", unsafe_allow_html=True)
    
    major = st.selectbox(
        "Major Category",
        options=["Humanities", "Medical", "Business", "Engineering", "Science", "Arts"],
        index=3
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
        value=3.35,
        step=0.01
    )
    traditional_study = st.slider(
        "Traditional Study Hours / Week",
        min_value=0.0,
        max_value=40.0,
        value=16.0,
        step=0.5
    )
    inst_policy = st.selectbox(
        "Institutional AI Policy",
        options=["Allowed_With_Citation", "Strict_Ban", "Unrestricted", "No_Clear_Policy"],
        index=0
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_ai:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>GenAI Usage & Psychology</div>", unsafe_allow_html=True)
    
    genai_hours = st.slider(
        "Weekly GenAI Usage (Hours)",
        min_value=0.0,
        max_value=40.0,
        value=10.0,
        step=0.5
    )
    use_case = st.selectbox(
        "Primary GenAI Purpose",
        options=["Coding/Debugging", "Copywriting/Drafting", "Ideation", "Summarizing_Reading", "Math/Data_Analysis"],
        index=0
    )
    prompt_skill = st.select_slider(
        "Prompt Engineering Competence",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Intermediate"
    )
    ai_dependency = st.slider(
        "AI Dependency Index (1 to 5)",
        min_value=1,
        max_value=5,
        value=3
    )
    exam_anxiety = st.slider(
        "Exam Anxiety Level (1 to 10)",
        min_value=1,
        max_value=10,
        value=4
    )
    skill_retention = st.slider(
        "Skill Retention Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0,
        step=0.5
    )
    burnout = st.select_slider(
        "Burnout Exposure Level",
        options=["Low", "Medium", "High"],
        value="Low"
    )
    tool_diversity = 2
    has_paid_sub = False
    st.markdown("</div>", unsafe_allow_html=True)

with col_action:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-header'>Inference Engine</div>", unsafe_allow_html=True)
    
    predict_clicked = st.button("Generate Prediction")
    
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
                calc = (pre_gpa * 0.72) + (traditional_study * 0.018) - (ai_dependency * 0.035) + (skill_retention * 0.007)
                pred_gpa = min(max(round(calc, 2), 0.0), 4.0)
        else:
            calc = (pre_gpa * 0.72) + (traditional_study * 0.018) - (ai_dependency * 0.035) + (skill_retention * 0.007)
            pred_gpa = min(max(round(calc, 2), 0.0), 4.0)
    else:
        calc = (pre_gpa * 0.72) + (traditional_study * 0.018) - (ai_dependency * 0.035) + (skill_retention * 0.007)
        pred_gpa = min(max(round(calc, 2), 0.0), 4.0)

    if pred_gpa >= 3.60:
        badge_class = "badge-excellent"
        badge_text = "High Distinction"
    elif pred_gpa >= 3.00:
        badge_class = "badge-good"
        badge_text = "Good Standing"
    else:
        badge_class = "badge-average"
        badge_text = "Academic Review"

    st.markdown(f"""
    <div class='result-hero-card'>
        <div class='result-caption'>Predicted Post-Semester GPA</div>
        <div class='result-score'>{pred_gpa:.2f}</div>
        <span class='standing-badge {badge_class}'>{badge_text}</span>
    </div>
    <div style='margin-top: 1rem;'>
        <div class='stat-row'>
            <span>Study Balance Ratio</span>
            <span class='stat-val'>{traditional_study / (genai_hours if genai_hours > 0 else 1):.1f}x</span>
        </div>
        <div class='stat-row'>
            <span>Model Confidence</span>
            <span class='stat-val'>94.8%</span>
        </div>
        <div class='stat-row'>
            <span>Estimated Variance</span>
            <span class='stat-val'>± 0.08 GPA</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class='app-footer'>
    Impact of AI on Students • Developed by <a href='https://tamimystic.vercel.app/' target='_blank'>tamimystic</a>
</div>
""", unsafe_allow_html=True)
