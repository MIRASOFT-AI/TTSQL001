import streamlit as st
import ast
import pandas as pd
import altair as alt
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Database Connection
db = SQLDatabase.from_uri("sqlite:///student_grades.db")

# Local LLM (Ollama)
llm = ChatOllama(
    model="llama3",
    temperature=0
)

# Prompt (LCEL Style)
prompt = ChatPromptTemplate.from_template("""
You are a senior data analyst and SQL expert.

Given the database schema below, write a correct SQL query
that answers the user's question.

Rules:
- Use only the tables and columns in the schema
- Do NOT explain anything
- Return ONLY the SQL query

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

        st.subheader("🧠 Generated SQL")
        st.code(sql_query, language="sql")

        st.subheader("📈 Result")
        result = db.run(sql_query)
        
        try:
            # Attempt to parse the string result into a list of tuples
            parsed_result = ast.literal_eval(result)
            if isinstance(parsed_result, list):
                if len(parsed_result) > 0:
                    # Create DataFrame
                    df = pd.DataFrame(parsed_result)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Query returned no results.")
            else:
                st.write(result)
        except (ValueError, SyntaxError):
            st.write(result)

    except Exception as e:
        st.error(f"❌ Error: {e}")

# Footer
st.markdown("---")
st.caption("Powered by LangChain 1.x • Ollama • Llama 3 • Streamlit")