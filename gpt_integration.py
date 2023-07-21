import openai
import sqlite3

openai.api_key = "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"

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

