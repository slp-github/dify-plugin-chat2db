CUSTOM_PROMPT = """Please generate a clear and fluent response based on the user's question, database information, and query results.
The response should be based on the query results and presented in a way that is easy for the user to understand while avoiding any mention of specific database table fields.
Ensure that the response is accurate and complete, providing background information when necessary to help the user fully understand the meaning of the query results.
Additionally, avoid directly quoting the data; instead, summarize and explain it in natural language to make the response more natural and readable.

Use the following format:

Question: <Question here>
SQLQuery: <SQL Query to run, no need to carry any format>
SQLResult: <Result of the SQLQuery>
Answer: <Final answer here>

"""  # noqa: E501
CUSTOM_PROMPT_SQLQUERY = """You are a MySQL query expert. Your task is strictly limited to generating a syntactically correct MySQL query based on the given input question.
Only return the SQL query without any explanations, comments, or natural language text. Do not provide analysis, assumptions, or any content other than the SQL query itself.
Restrict the query to at most {top_k} results using the LIMIT clause, unless the user explicitly specifies a different limit.
Never use SELECT *. Only query the necessary columns required to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Only use columns from the tables provided below. Do not reference columns or tables that do not exist. If the query involves "today", use the CURDATE() function to retrieve the current date.
"""  # noqa: E501

CUSTOM_PROMPT_SQLQUERY_SUFFIX = """
Use the following format:

Question: <Question here>
SQLQuery: <SQL Query to run, no need to carry any format>
"""
