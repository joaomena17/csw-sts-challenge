import openai
import sqlite3

def generate_sql_query(table1, table2, columns1, columns2, text):
    prompt = """ETC... 
    The table names are {} and {} and the corresponding \
    columns are {} and {}.\Input: {}\nSQL Query:""".format(
        table1, table2, columns1, columns2, text
    )

request = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo-0301",
    messages = [
        {"role": "user", "content": prompt}
    ]
)

sql_query = request["choices"][0]["message"]["content"]

return sql_query