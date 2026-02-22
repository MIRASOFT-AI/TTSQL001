import streamlit as st
import os
import ast
import pandas as pd
import altair as alt
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv() # This loads local .env files if they exist
api_key = os.getenv("GOOGLE_API_KEY") # This reads from the system environment

# Database Connection
db = SQLDatabase.from_uri("sqlite:///student_grades.db")

# Cloud LLM (Google Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=api_key,
    temperature=0,
    convert_system_message_to_human=True
)

# Prompt (LCEL Style)
prompt = ChatPromptTemplate.from_template("""
You are a senior data analyst and SQL expert.

Given the database schema below, write a correct SQL query
that answers the user's question.

Rules:
- Use only the tables and columns in the schema
- Do NOT explain anything
- Return ONLY the SQL query to execute directly on the database without any modifications

Schema:
{schema}

Question:
{question}
""")

# LCEL Runnable Pipeline
sql_chain = (
    prompt
    | llm
    | StrOutputParser()
)

schema = db.get_table_info()

# Page Setup
st.set_page_config(page_title="Text-to-SQL App", layout="centered")
st.title("📊 Talk to Your Database")
st.write("Ask questions about the student grades database in plain English.")


# UI Input
question = st.text_input(
    "Enter your question:",
    placeholder="e.g., Who scored the highest in Math?"
)

# Execution
if question:
    try:
        sql_query = sql_chain.invoke(
            {"schema": schema, "question": question}
        ).strip()

        print(f"Generated SQL: {sql_query}")
        st.subheader("🧠 Generated SQL")
        st.code(sql_query, language="sql")

        st.subheader("📈 Result")
        result = db.run(sql_query)
        
        try:
            # Attempt to parse the string result into a list of tuples
            parsed_result = ast.literal_eval(result)
            if isinstance(parsed_result, list) and len(parsed_result) > 0:
                # Create DataFrame
                df = pd.DataFrame(parsed_result)
                
                # --- Visualization Section ---
                tab1, tab2, tab3 = st.tabs(["📄 Table", "📈 Line Chart", "🥧 Pie Chart"])
                
                with tab1:
                    st.dataframe(df, use_container_width=True)
                
                with tab2:
                    if len(df.columns) >= 2:
                        # Try to find numeric columns for Y axis
                        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                        all_cols = df.columns.tolist()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            x_axis = st.selectbox("Select X axis:", all_cols, index=0, key="line_x")
                        with col2:
                            y_axis = st.selectbox("Select Y axis:", numeric_cols if numeric_cols else all_cols, index=0, key="line_y")
                        
                        st.line_chart(df.set_index(x_axis)[y_axis])
                    else:
                        st.warning("Not enough columns for a line chart (need at least 2).")
                
                with tab3:
                    if len(df.columns) >= 2:
                        col1, col2 = st.columns(2)
                        with col1:
                            category_col = st.selectbox("Select Category:", df.columns, index=1, key="pie_cat")
                        with col2:
                            value_col = st.selectbox("Select Value:", df.select_dtypes(include=['number']).columns if not df.select_dtypes(include=['number']).empty else df.columns, index=0, key="pie_val")
                        
                        pie_chart = alt.Chart(df).mark_arc().encode(
                            theta=alt.Theta(field=value_col, type="quantitative"),
                            color=alt.Color(field=category_col, type="nominal"),
                            tooltip=[category_col, value_col]
                        ).properties(width=400, height=400)
                        
                        st.altair_chart(pie_chart, use_container_width=True)
                    else:
                        st.warning("Not enough columns for a pie chart.")
                # --- End Visualization Section ---
                
            else:
                st.write(result)
        except (ValueError, SyntaxError):
            # If parsing fails (e.g., result is a single value or message), show as text
            st.write(result)

    except Exception as e:
        st.error(f"❌ Error: {e}")

# Footer
st.markdown("---")
st.caption("Powered by LangChain 1.x • Google Gemini • Streamlit")