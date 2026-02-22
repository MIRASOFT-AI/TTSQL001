# Text-to-SQL App

This project is a Streamlit-based application that allows users to interact with a SQLite database using natural language. It leverages LangChain and Large Language Models (LLMs) to convert English questions into SQL queries, executes them against a database, and visualizes the results.

The project is based on the guide: https://amanxai.com/2026/02/08/build-your-first-text-to-sql-app/

## Project Structure

- `app.py`: Local version of the application using **Ollama** (Llama 3).
- `cloud.py`: Cloud version of the application using **Google Gemini**.
- `create_db.py`: Python script to initialize the SQLite database (`student_grades.db`) with sample data.
- `requirements.txt`: List of Python dependencies.
- `Steps.me`: Quick reference for environment setup and execution commands.
- `.env`: (Optional) Environment variables for API keys (e.g., `GOOGLE_API_KEY`).

## Features

- **Natural Language Querying**: Ask questions like "Who scored the highest in Math?" and get SQL results.
- **Schema Awareness**: The LLM uses the database schema to generate accurate queries.
- **Data Visualization**: Results are displayed in a table and can be visualized using Bar Charts or Pie Charts.
- **Dual Support**: Supports both local (Ollama) and cloud (Gemini) LLM providers.

## Getting Started

### 1. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
.\venv\Scripts\Activate  # On Windows
pip install -r requirements.txt
```

### 2. Database Initialization
Run the script to create the `student_grades.db` database:
```bash
python create_db.py
```

### 3. Running the App

#### Local Version (Ollama)
Ensure Ollama is running with the `llama3` model:
```bash
streamlit run app.py
```

#### Cloud Version (Gemini)
Ensure you have a `.env` file with your `GOOGLE_API_KEY`:
```bash
streamlit run cloud.py
```

## Technologies Used

- **Streamlit**: Web UI Framework.
- **LangChain**: LLM Orchestration (LCEL).
- **Ollama / Google Gemini**: LLM Providers.
- **SQLite**: Database Engine.
- **Pandas & Altair**: Data Processing and Visualization.
