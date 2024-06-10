from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

llm_file_path = '../models/Phi-3-mini-4k-instruct-q4.gguf'
prompt = """### Task
Generate Database Schema to store data mentioned in [QUESTION]{question}[/QUESTION]

### Instructions
- SQL Dialect is SQLite
- Also generate sample SELECT queries for this schema 
"""

callback = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    model_path=llm_file_path,
    n_ctx=4096,
    temperature=0,
    seed=4381,
    max_tokens=10000,
    verbose=True,  # Verbose is required to pass to the callback manager
    streaming=True,
    callback_manager=callback
)


# Scenarios generates via Llama 3 via following input :
# A professor teaches RDBMS for a Computer Science school. He needs to prepare a DB schema design assignment with 20
# questions. Each question should describe a real world scenario and requires a DB schema DDL. Scenario requires
# students to think of database entities and write DB schema DDLs. Entities should have some one-to-many and at least
# one many-to-many relationship. Write those 20 questions.
#
#

question1 = ("Create a database schema for a university management system that stores information about students, "
             "courses, instructors, and departments.")

question2 = """
Design a database schema for an online shopping platform that allows customers to create accounts, place orders, 
and track their order history.

Add a feature to allow customers to leave reviews for products they've purchased.

Store product categories (e.g., electronics, clothing, home goods). Categories can be hierarchical. 

Allow customers to add products to their wishlists.

Store order details, including shipping information and payment methods.
"""

question3 = """
Create a database schema for a social media platform that allows users to create profiles, post updates, 
and follow other users.

Include a table to store user friendships (e.g., who is following whom).

Store posts, including comments and likes.

Allow users to upload profile pictures and cover photos.

Create a table to store trending topics and hashtags.
"""

question4 = """
Design a database schema for a travel agency that allows customers to book flights, hotels, and rental cars.

Include a table to store customer information (e.g., name, email, phone number).

Create tables to store flight information, flight schedules and availability.

Allow customers to create and manage their own itineraries.

Design a table to store travel reviews and ratings.
"""

questions = [question1, question2, question3, question4]

for q in questions:
    inp = prompt.format(question=q)
    output = llm.invoke(inp)
    print(output)
    print('\n\n\n')
