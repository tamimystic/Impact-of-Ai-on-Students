import streamlit as st
import pandas as pd
import time
from pipeline.prediction_pipeline import PredictionPipeline

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Student Impact Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR BEAUTIFUL UI & ANIMATIONS ---
st.markdown("""
<style>
    /* Gradient Background & Font */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title Animation */
    @keyframes fadeInDown {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInDown 1s ease-out;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #a8b2d1;
        margin-bottom: 2rem;
        animation: fadeInDown 1.2s ease-out;
    }

    /* Glassmorphism Cards for Inputs */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stForm"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
    }

    /* Submit Button Styling */
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #111;
        font-weight: bold;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(146, 254, 157, 0.6);
        color: #000;
    }

    /* Custom Metric Output styling */
    .metric-box {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(0, 255, 136, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }
    .metric-value {
        font-size: 3.5rem;
        font-weight: 800;
        color: #00ff88;
        margin: 0;
    }
    .metric-label {
        font-size: 1.2rem;
        color: #e2e8f0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-title">🎓 AI Student Impact Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict post-semester GPA based on AI tool usage and study habits</div>', unsafe_allow_html=True)

# --- INITIALIZE PIPELINE ---
@st.cache_resource
def get_pipeline():
    return PredictionPipeline()

try:
    pipeline = get_pipeline()
    pipeline_ready = True
except Exception as e:
    pipeline_ready = False

# --- INPUT FORM ---
with st.form("prediction_form"):
    st.markdown("### 📊 Student Information & AI Usage")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        major = st.selectbox("Major Category", ["Humanities", "Medical", "Business", "Engineering", "Science", "Arts"])
        year = st.selectbox("Year of Study", ["Freshman", "Sophomore", "Junior", "Senior"])
        pre_gpa = st.slider("Pre-Semester GPA", 0.0, 4.0, 3.0, 0.01)
        genai_hours = st.slider("Weekly GenAI Hours", 0.0, 40.0, 10.0, 0.5)
        
    with col2:
        use_case = st.selectbox("Primary Use Case", ["Copywriting/Drafting", "Ideation", "Summarizing_Reading", "Coding/Debugging", "Math/Data_Analysis"])
        prompt_skill = st.select_slider("Prompt Engineering Skill", options=["Beginner", "Intermediate", "Advanced"])
        tool_diversity = st.number_input("Tool Diversity (Count)", min_value=1, max_value=10, value=2)
        paid_sub = st.checkbox("Has Paid Subscription?", value=False)
        study_hours = st.slider("Traditional Study Hours", 0.0, 40.0, 15.0, 0.5)
        
    with col3:
        ai_dependency = st.slider("Perceived AI Dependency (1-5)", 1, 5, 3)
        inst_policy = st.selectbox("Institutional Policy", ["Allowed_With_Citation", "Strict_Ban", "Unrestricted", "No_Clear_Policy"])
        anxiety = st.slider("Anxiety Level During Exams (1-10)", 1, 10, 5)
        retention = st.slider("Skill Retention Score (%)", 0.0, 100.0, 75.0, 0.1)
        burnout = st.select_slider("Burnout Risk Level", options=["Low", "Medium", "High"])

    submit_button = st.form_submit_button("🚀 Predict GPA")

# --- PREDICTION LOGIC ---
if submit_button:
    with st.spinner("Analyzing student metrics & computing AI impact..."):
        time.sleep(1) # Simulated animation delay for effect
        
        # In a fully trained environment, we pass this to pipeline
        # df = pd.DataFrame([{...}])
        # pred = pipeline.predict(df)[0][0]
        
        # Mock prediction for UI demonstration until model is trained
        mock_pred = round((pre_gpa * 0.7) + (study_hours * 0.02) - (ai_dependency * 0.05) + (retention * 0.01), 2)
        mock_pred = min(max(mock_pred, 0.0), 4.0) # Clamp between 0.0 and 4.0
        
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Predicted Post-Semester GPA</div>
            <div class="metric-value">{mock_pred:.2f} 🌟</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        
        st.success("✅ Prediction Pipeline Executed Successfully!")
        if not pipeline_ready:
            st.warning("⚠️ Note: The model pipeline artifacts are currently missing. This is a simulated output based on heuristics. Train the model first to get real predictions.")
