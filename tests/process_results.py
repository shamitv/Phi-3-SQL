from dao.query_manager import QueryManager

# Specify the path to the SQLite database
database_path = "../data/query_tasks.sqlite"
query_manager = QueryManager(database_path)  # Initialize QueryManager here. Add necessary arguments if needed.
unfinished_task = query_manager.get_unfinished_task()  # Get the unfinished task

print(unfinished_task)
# Do something with the unfinished task here
