# Python file: query_manager.py
import sqlite3


class QueryManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Create table if it doesn't exist
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS queries 
                    (   id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Entity TEXT NOT NULL,
                        start_time REAL,
                        end_time REAL,
                        llm_question TEXT,
                        llm_input TEXT,
                        llm_output TEXT,
                        extracted_query TEXT,
                        task_done BOOLEAN DEFAULT FALSE
                    )
                ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def insert_query(self, entity, start_time, end_time, llm_output, extracted_query, task_done, llm_question,
                     llm_input):
        cur = self.conn.cursor()
        query = """
                INSERT INTO queries 
                (Entity, start_time, end_time, llm_output, extracted_query, task_done, llm_question, llm_input)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
        cur.execute(query,
                    (entity, start_time, end_time, llm_output, extracted_query,
                     task_done, llm_question, llm_input))
        self.conn.commit()
        return cur.lastrowid

    def get_unfinished_task(self):
        cur = self.conn.cursor()
        query = """
            SELECT * FROM queries 
            WHERE task_done = 0 
            ORDER BY ID ASC 
            LIMIT 1;    
        """
        cur.execute(query)
        row = cur.fetchone()

        if row is None:
            return None
        col_names = [desc[0] for desc in cur.description]
        return dict(zip(col_names, row))

    def get_by_id(self, id):
        cur = self.conn.cursor()
        query = "SELECT * FROM queries WHERE ID = ?"
        cur.execute(query, (id,))
        row = cur.fetchone()

        if row is None:
            return None
        col_names = [desc[0] for desc in cur.description]
        return dict(zip(col_names, row))