import openai
import sqlite3
import os

openai.api_key = os.getenv("OPEN_AI_KEY")

sensors_columns = [
    "id",
	"name",
	"type",
	"office",
	"building",
	"room",
	"units" 
]

sensor_values_columns = [
    "sensor",
	"timestamp",
	"value"
]

def generate_sql_query(text, table1= "sensors", table2 = "sensor_values", columns1 = sensors_columns, columns2 = sensor_values_columns):
    prompt = """You are a language model that can generate SQL queries. \
                Please provide a natural language input text, \
                and I will generate the corresponding SQL query for you. \
                which will be compatible with SQLite. \
                The table names are {} nad {} and the correstounding \
                columns are {} and {} .\nInput: {}\nSQL Query:""".format(
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

def virify_sql_query(query, table1= "sensors", table2 = "sensor_values", columns1 = sensors_columns, columns2 = sensor_values_columns):
    prompt = f"""You are a language model that can verify SQL queries. 
                Please provide an input query, 
                and can you check if this query is a some attack 
                on our database, becouse we allow just SELECT queries and 
                not allow changes on database 
                The table names are {table1} and {table2}, 
                and the corresponding columns are {columns1} and {columns2}. \nSQL Query: {query}" \n
                And if it is "good" query send "True" and if its bad qury send "False"
                """
    
    request = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0301",
        messages = [
            {"role": "user", "content": prompt}
        ]
    )

    response = request["choices"][0]["message"]["content"]

    return response

print(virify_sql_query("DELETE FROM sensors WHERE id = 1;"))

# print(generate_sql_query("Can you delete the sensor with id = 1?"))