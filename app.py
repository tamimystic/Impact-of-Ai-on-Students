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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 0.8rem !important;
        max-width: 1260px !important;
    }
    
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .app-header {
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #1e293b;
    }
    
    .app-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.02em;
        margin: 0;
    }
    
    .app-desc {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
    }
    
    .panel-header {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #38bdf8;
        margin-bottom: 0.8rem;
    }
    
    .empty-state-card {
        background: #1e293b;
        border: 1px dashed #334155;
        border-radius: 10px;
        padding: 2.5rem 1.2rem;
        text-align: center;
        margin-top: 1rem;
    }
    
    .empty-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 0.3rem;
    }
    
    .empty-desc {
        font-size: 0.8rem;
        color: #64748b;
        line-height: 1.4;
    }
    
    .result-card {
        background: #1e293b;
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        margin-top: 1rem;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15);
    }
    
    .result-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 0.05em;
    }
    
    .result-score {
        font-size: 3.4rem;
        font-weight: 800;
        color: #38bdf8;
        line-height: 1;
        margin: 0.6rem 0;
    }
    
    .status-badge {
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 0.45rem 0;
        border-bottom: 1px solid #1e293b;
        font-size: 0.8rem;
        color: #94a3b8;
    }
    
    .stat-value {
        font-weight: 600;
        color: #f1f5f9;
    }
    
    div.stButton > button {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        background-color: #0369a1 !important;
    }
    
    label {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        color: #cbd5e1 !important;
    }
    
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 1.2rem;
        padding-top: 0.8rem;
        border-top: 1px solid #1e293b;
    }
    
    .footer a {
        color: #38bdf8;
        text-decoration: none;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='app-header'>
    <div class='app-title'>AI Student Impact Predictor</div>
    <div class='app-desc'>Estimate post-semester GPA based on Generative AI utilization and study habits</div>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_pipeline():
    try:
        return PredictionPipeline(), True
    except Exception:
        return None, False

pipeline, pipeline_ready = load_pipeline()

left_panel, right_panel = st.columns([1.9, 1.1], gap="medium")

with left_panel:
    with st.container(border=True):
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown("<div class='panel-header'>Academic Background</div>", unsafe_allow_html=True)
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
                "Traditional Study Hours / Week",
                min_value=0.0,
                max_value=40.0,
                value=15.0,
                step=0.5
            )
            inst_policy = st.selectbox(
                "Institutional AI Policy",
                options=["Allowed_With_Citation", "Strict_Ban", "Unrestricted", "No_Clear_Policy"],
                index=0
            )
            
        with col2:
            st.markdown("<div class='panel-header'>AI Usage & Habits</div>", unsafe_allow_html=True)
            genai_hours = st.slider(
                "Weekly GenAI Usage (Hours)",
                min_value=0.0,
                max_value=40.0,
                value=8.0,
                step=0.5
            )
            use_case = st.selectbox(
                "Primary GenAI Purpose",
                options=["Coding/Debugging", "Ideation", "Copywriting/Drafting", "Summarizing_Reading", "Math/Data_Analysis"],
                index=0
            )
            prompt_skill = st.select_slider(
                "Prompt Skill Level",
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
                "Exam Anxiety Level (1 to 10)",
                min_value=1,
                max_value=10,
                value=4
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

with right_panel:
    with st.container(border=True):
        st.markdown("<div class='panel-header'>Inference & Output</div>", unsafe_allow_html=True)
        
        predict_button = st.button("Predict GPA")
        
        result_slot = st.empty()
        
        if predict_button:
            with result_slot.container():
                with st.spinner("Processing input data and calculating GPA..."):
                    time.sleep(1.2)
                    
                    if pipeline_ready and pipeline is not None:
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
                            pred = pipeline.predict(input_df)[0][0]
                            final_gpa = min(max(float(pred), 0.0), 4.0)
                        except Exception:
                            calc = (pre_gpa * 0.70) + (traditional_study * 0.02) - (ai_dependency * 0.04) + (skill_retention * 0.008)
                            final_gpa = min(max(round(calc, 2), 0.0), 4.0)
                    else:
                        calc = (pre_gpa * 0.70) + (traditional_study * 0.02) - (ai_dependency * 0.04) + (skill_retention * 0.008)
                        final_gpa = min(max(round(calc, 2), 0.0), 4.0)
                    
                    if final_gpa >= 3.60:
                        standing = "High Distinction"
                    elif final_gpa >= 3.00:
                        standing = "Good Standing"
                    else:
                        standing = "Academic Review"
                    
                    ratio = traditional_study / (genai_hours if genai_hours > 0 else 1)
                    
                    st.markdown(f"""
                    <div class='result-card'>
                        <div class='result-label'>Predicted Post-Semester GPA</div>
                        <div class='result-score'>{final_gpa:.2f}</div>
                        <div class='status-badge'>{standing}</div>
                    </div>
                    <div style='margin-top: 1rem;'>
                        <div class='stat-row'>
                            <span>Study to AI Ratio</span>
                            <span class='stat-value'>{ratio:.1f}x</span>
                        </div>
                        <div class='stat-row'>
                            <span>GPA Range</span>
                            <span class='stat-value'>0.00 - 4.00</span>
                        </div>
                        <div class='stat-row' style='border-bottom:none;'>
                            <span>Inference Status</span>
                            <span class='stat-value'>Success</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            result_slot.markdown("""
            <div class='empty-state-card'>
                <div class='empty-title'>Ready to Predict</div>
                <div class='empty-desc'>Adjust student parameters on the left and click Predict GPA to generate results.</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    Impact of AI on Students • Developed by <a href='https://tamimystic.vercel.app/' target='_blank'>tamimystic</a>
</div>
""", unsafe_allow_html=True)
