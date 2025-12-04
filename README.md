# Data Science Lab Spring 2024

This is a project co-developed with the company Breathe Medical to generate customizable medical training scenarios for low-resource hospitals using LLM's. Our interface is shown below.

<img aling="center" width="1701" height="958" alt="dashboard-example" src="https://github.com/user-attachments/assets/4cec3612-dff5-48fd-ad77-c3e0eb55c8e9" />




## Get started

### 1. Create a Python environment (skip this step if you are not setting this up for the first time)

```
python3.12 -m venv dsl
```

### 2. Activate the Python environment

```
source dsl/bin/activate
```

### 3. Install dependencies (only for first time setup or if something has changed)

```
pip install -r requirements.txt
```

### 4. Set up environment file

Duplicate the `.env.example` file, rename it to `.env` and add your OpenAI API key.

### 5. Run scenario generator (Streamlit app)

```
streamlit run app.py
```
