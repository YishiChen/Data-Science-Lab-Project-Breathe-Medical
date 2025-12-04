# Data Science Lab Spring 2024

This is a project co-developed with the company breathe to generate customizable medical scenarios for low-resource hospitals.

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
