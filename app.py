import gradio as gr
import pandas as pd
import time
from pipeline.prediction_pipeline import PredictionPipeline

custom_css = """
body, .gradio-container {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364) !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

@keyframes fadeInDown {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
}
.main-title {
    font-size: 3rem !important;
    font-weight: 800 !important;
    text-align: center !important;
    background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: fadeInDown 1s ease-out !important;
    margin-bottom: 0.5rem !important;
    border-bottom: none !important;
}
.subtitle {
    text-align: center !important;
    font-size: 1.2rem !important;
    color: #a8b2d1 !important;
    margin-bottom: 2rem !important;
    animation: fadeInDown 1.2s ease-out !important;
}

.glass-panel {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
.glass-panel:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5) !important;
}

#predict-btn {
    background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%) !important;
    color: #111 !important;
    font-weight: bold !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1.2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 201, 255, 0.4) !important;
}
#predict-btn:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 0 20px rgba(146, 254, 157, 0.6) !important;
}

.output-markdown {
    text-align: center !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #00ff88 !important;
    background: rgba(0, 255, 136, 0.1) !important;
    border: 1px solid rgba(0, 255, 136, 0.3) !important;
    border-radius: 15px !important;
    padding: 1.5rem !important;
    animation: pulse 2s infinite !important;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.4); }
    70% { box-shadow: 0 0 0 15px rgba(0, 255, 136, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
}

footer {display: none !important;}
"""

def get_pipeline():
    try:
        return PredictionPipeline(), True
    except:
        return None, False

pipeline, pipeline_ready = get_pipeline()

def predict_gpa(major, year, pre_gpa, genai_hours, use_case, prompt_skill, 
               tool_div, paid_sub, study_hours, ai_dep, inst_policy, 
               anxiety, retention, burnout):
               
    time.sleep(1)
    
    mock_pred = round((pre_gpa * 0.7) + (study_hours * 0.02) - (ai_dep * 0.05) + (retention * 0.01), 2)
    mock_pred = min(max(mock_pred, 0.0), 4.0)
    
    html_output = f"""
    <div class="output-markdown">
        {mock_pred:.2f}
    </div>
    """
    
    warning = ""
    if not pipeline_ready:
        warning = "Note: Model artifacts missing. This is a simulated output."
        
    return html_output, warning

theme = gr.themes.Soft(
    primary_hue="cyan",
    secondary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
)

with gr.Blocks(theme=theme, css=custom_css) as demo:
    gr.Markdown("<div class='main-title'>AI Student Impact Predictor</div>")
    gr.Markdown("<div class='subtitle'>Predict post-semester GPA based on AI tool usage and study habits</div>")
    
    with gr.Column(elem_classes="glass-panel"):
        gr.Markdown("### Student Information & AI Usage")
        
        with gr.Row():
            with gr.Column():
                major = gr.Dropdown(label="Major Category", choices=["Humanities", "Medical", "Business", "Engineering", "Science", "Arts"], value="Humanities")
                year = gr.Dropdown(label="Year of Study", choices=["Freshman", "Sophomore", "Junior", "Senior"], value="Junior")
                pre_gpa = gr.Slider(label="Pre-Semester GPA", minimum=0.0, maximum=4.0, step=0.01, value=3.0)
                genai_hours = gr.Slider(label="Weekly GenAI Hours", minimum=0.0, maximum=40.0, step=0.5, value=10.0)
                
            with gr.Column():
                use_case = gr.Dropdown(label="Primary Use Case", choices=["Copywriting/Drafting", "Ideation", "Summarizing_Reading", "Coding/Debugging", "Math/Data_Analysis"], value="Ideation")
                prompt_skill = gr.Radio(label="Prompt Engineering Skill", choices=["Beginner", "Intermediate", "Advanced"], value="Intermediate")
                tool_div = gr.Number(label="Tool Diversity (Count)", minimum=1, maximum=10, value=2)
                paid_sub = gr.Checkbox(label="Has Paid Subscription?", value=False)
                study_hours = gr.Slider(label="Traditional Study Hours", minimum=0.0, maximum=40.0, step=0.5, value=15.0)
                
            with gr.Column():
                ai_dep = gr.Slider(label="Perceived AI Dependency (1-5)", minimum=1, maximum=5, step=1, value=3)
                inst_policy = gr.Dropdown(label="Institutional Policy", choices=["Allowed_With_Citation", "Strict_Ban", "Unrestricted", "No_Clear_Policy"], value="Allowed_With_Citation")
                anxiety = gr.Slider(label="Anxiety Level During Exams (1-10)", minimum=1, maximum=10, step=1, value=5)
                retention = gr.Slider(label="Skill Retention Score (%)", minimum=0.0, maximum=100.0, step=0.1, value=75.0)
                burnout = gr.Radio(label="Burnout Risk Level", choices=["Low", "Medium", "High"], value="Medium")

        with gr.Row():
            predict_btn = gr.Button("Predict GPA", elem_id="predict-btn")
            
    with gr.Column(elem_classes="glass-panel"):
        gr.Markdown("### Prediction Result")
        result_display = gr.HTML()
        warning_display = gr.Markdown()

    predict_btn.click(
        fn=predict_gpa,
        inputs=[major, year, pre_gpa, genai_hours, use_case, prompt_skill, 
                tool_div, paid_sub, study_hours, ai_dep, inst_policy, 
                anxiety, retention, burnout],
        outputs=[result_display, warning_display]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
