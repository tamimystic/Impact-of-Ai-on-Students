---
title: Impact of Ai on Students
emoji: 🎓
colorFrom: blue
colorTo: blue
sdk: gradio
sdk_version: 4.42.0
app_file: app.py
pinned: false
---

# AI Student Impact Predictor

Live Application: [https://huggingface.co/spaces/tamimystic/Impact-of-Ai-on-Students](https://huggingface.co/spaces/tamimystic/Impact-of-Ai-on-Students)

This is an End-to-End Machine Learning project designed to predict a student's post-semester GPA based on their study habits and usage of Generative AI tools. 

---

## For Users: How to Use the Application

If you are a student, educator, or researcher, you can use this tool to understand how different habits impact academic performance.

Steps to use:
1. Visit the Live Application link above.
2. In the Student Information & AI Usage section, fill out your current metrics:
   - Academic Details: Select your Major, Year of Study, and Pre-Semester GPA.
   - AI Usage: Input your weekly hours spent on GenAI, your primary use case, and your prompt engineering skill level.
   - Habits & Psychology: Provide your traditional study hours, perceived dependency on AI, and anxiety levels.
3. Click the Predict GPA button.
4. The system will process your inputs and display your predicted Post-Semester GPA in the result panel.

---

## For Developers: Project Architecture & Workflow

This project is built following strict Industry-Standard Modular ML Architecture. It is designed to be highly scalable, maintainable, and easy to integrate with CI/CD pipelines.

### End-to-End Workflow

The project is structured into independent components, each responsible for a specific stage of the machine learning lifecycle. These components are orchestrated by pipelines.

#### 1. Data Ingestion (components/data_ingestion.py)
- Action: Connects to a remote MongoDB Atlas cluster.
- Process: Retrieves the raw dataset dynamically and converts it into a Pandas DataFrame.
- Output: Performs a train-test split and saves the resulting files into the artifacts/data_ingestion directory.

#### 2. Data Validation (components/data_validation.py)
- Action: Validates the ingested data.
- Process: Checks schema, data types, and ensures no structural anomalies exist before preprocessing.

#### 3. Data Transformation (components/data_transformation.py)
- Action: Prepares the data for model consumption.
- Process: Applies specific Scikit-Learn transformers:
  - LabelEncoder: For categorical columns.
  - OrdinalEncoder: For ranked features.
  - StandardScaler: Scales numerical features to standard distributions.
- Output: Saves the transformed NumPy arrays and the preprocessing pipeline object into artifacts/data_transformation.

#### 4. Model Trainer & Wrapping (components/model_trainer.py)
- Action: Prepares the Keras model.
- Process: Instead of training from scratch on every pipeline run, this component is configured to ingest a pre-trained keras model from the models directory.

#### 5. Model Evaluation & Pusher (components/model_evaluation.py & components/model_pusher.py)
- Action: Evaluates performance and pushes artifacts.
- Process: Checks the model's metrics against baseline thresholds. Upon acceptance, the model and the preprocessor object are pushed to the saved_models directory.

#### 6. Prediction Pipeline & UI (pipeline/prediction_pipeline.py & app.py)
- Action: Handles real-time inference.
- Process: The PredictionPipeline loads the artifacts from saved_models, takes user inputs, scales them using the loaded preprocessor, and feeds them into the Keras model.
- UI: The frontend is built with Gradio, heavily customized with advanced CSS to provide a premium user experience.

### CI/CD Deployment Strategy
- The repository utilizes GitHub Actions.
- Whenever code is pushed to the main branch, the workflow automatically authenticates via OAuth2 tokens and syncs the entire repository to Hugging Face Spaces.

### How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/tamimystic/Impact-of-Ai-on-Students.git
   cd Impact-of-Ai-on-Students
   ```
2. Create and activate a virtual environment.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your .env file with MongoDB credentials:
   ```env
   MONGO_DB_URL="your_mongodb_connection_string"
   ```
5. Dump initial data to MongoDB:
   ```bash
   python data_dump.py
   ```
6. Run the application:
   ```bash
   python app.py
   ```