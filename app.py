import dash
from dash import html
from app.db import get_sql_connection

app = dash.Dash(__name__)
    
# This is test code for testing supabase connection
# Should move away once we start creatign actual functionality...
conn = get_sql_connection()

if conn is None:
    app.layout = html.Div("Error: Unable to connect to the database.")
else:
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()

        print("Current Time:", result[0])  

        app.layout = html.Div(f"Current time: {result[0]}")

    except Exception as e:
        print("Database query error:", e)
        app.layout = html.Div("Error: Unable to fetch time from database.")
    
    finally:
        cursor.close()
        conn.close()
    
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8000)

