import dash
from dash import html
from app.databases.psql_db import get_sql_connection
from app.databases.neo4j_db import run_query

app = dash.Dash(__name__)
    
# This is test code for testing supabase connection
# Should move away once we start creatign actual functionality...
conn = get_sql_connection()

psql_status = "Error: Unable to connect to Supabase."
if conn:
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("Supabase Current Time:", result[0])  

        psql_status = f"Supabase Current Time: {result[0]}"

    except Exception as e:
        print("Supabase query error:", e)
        psql_status = "Error: Unable to fetch time from Supabase."

    finally:
        cursor.close()
        conn.close()

# Test Neo4j Connection 
neo4j_status = "Error: Unable to connect to Neo4j."
try:
    result = run_query("MATCH (n) RETURN count(n) AS node_count")
    node_count = result[0]['node_count'] if result else 0
    print(f"Neo4j Node Count: {node_count}")
    
    neo4j_status = f"Neo4j Node Count: {node_count}"

except Exception as e:
    print("Neo4j connection error:", e)
    neo4j_status = "Error: Unable to fetch data from Neo4j."

# Define Test Dash Layout
app.layout = html.Div([
    html.H1("Database Connection Test"),
    html.P(psql_status),
    html.P(neo4j_status)
])

# --- Run Dash App ---
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8000)

