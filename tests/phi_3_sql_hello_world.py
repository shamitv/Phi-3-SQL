from langchain_community.llms import LlamaCpp
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine


prompt = """### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]

### Instructions
- If you cannot answer the question with the available database schema, return 'I do not know'
- SQL Dialect is SQLite
- Generate only one variation of query
- Do not suggest alternative varions for the query 

### Database Schema
This query will run on a database whose schema is represented in this string:
{db_schema}
### Answer
Given the database schema, here is the SQL query that answers [QUESTION]{question}[/QUESTION]
[SQL]
"""

db_file_path = '../data/Chinook_Sqlite.sqlite'
db_uri = "sqlite:///" + db_file_path
db = SQLDatabase.from_uri(db_uri,sample_rows_in_table_info=0)
db_engine = create_engine(db_uri)
db_schema_str = db.get_table_info()

llm_file_path = '../models/Phi-3-mini-4k-instruct-q4.gguf'

llm = LlamaCpp(
        model_path=llm_file_path,
        n_ctx=4096,
        temperature=0,
        seed=4381,
        max_tokens=4000
    )

inp = prompt.format(question="Which customer generated max sales?",db_schema=db_schema_str)
output = llm.invoke(inp)

print(output)
