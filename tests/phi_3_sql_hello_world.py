import logging
import time

from langchain_community.llms import LlamaCpp
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from dao import QueryManager

# create QueryManager instance
query_manager = QueryManager("sql_stats.sqlite")

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

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

--salesperson is same as Employee
"""

db_file_path = '../data/Chinook_Sqlite.sqlite'
db_uri = "sqlite:///" + db_file_path
db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=0)
db_engine = create_engine(db_uri)
db_schema_str = db.get_table_info()

llm_file_path = '../models/Phi-3-mini-4k-instruct-q4.gguf'

llm = LlamaCpp(
    model_path=llm_file_path,
    n_ctx=4096,
    temperature=0,
    seed=4381,
    max_tokens=4000,
    verbose=False,
    n_gpu_layers=1
)

entities = ['client', 'customer', 'artist', 'track', 'album', 'genre', 'playlist', 'salesperson', 'employee']

# Specify the path to the SQLite database
database_path = "../data/query_tasks.sqlite"

# Create QueryManager instance
query_manager = QueryManager(database_path)

for entity in entities:
    start_time = time.time()
    qry = "Which " + entity + " generated max sales?"
    logger.info(qry)

    inp = prompt.format(question=qry, db_schema=db_schema_str)
    output = llm.invoke(inp)
    end_time = time.time()
    query_manager.insert_query(entity=entity, start_time=start_time, end_time=end_time, llm_output=output,
                               task_done=False, extracted_query=None, llm_input=inp, llm_question=qry)

    start_time = time.time()
    qry = "How many " + entity + " exist?"
    logger.info(qry)

    inp = prompt.format(question=qry, db_schema=db_schema_str)
    output = llm.invoke(inp)
    end_time = time.time()
    query_manager.insert_query(entity=entity, start_time=start_time, end_time=end_time, llm_output=output,
                               task_done=False, extracted_query=None, llm_input=inp, llm_question=qry)
    #print(output)
