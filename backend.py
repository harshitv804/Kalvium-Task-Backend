# Kalvium Task Backend
# Harshit V
# SRM Institute Of Science And Technology Ramapuram

from flask import Flask, request, jsonify
import sqlite3

# Initialize SQLite database
conn = sqlite3.connect('history.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table to store the history if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
''')

app = Flask(__name__)

# Helper function to perform mathematical operations
def calculate_expression(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

@app.route('/<path:expression>', methods=['GET'])

def perform_operation(expression):
    if expression == 'favicon.ico':
        return ""
    # Replace keywords with symbols
    expression = expression.replace('plus', '+').replace('minus', '-').replace('into', '*').replace('dividedby', '/')

    # Split the expression by '/'
    parts = expression.split('/')

    # Build the math expression from the URL
    math_expression = ''.join(parts)

    # Calculate the result
    result = calculate_expression(math_expression)

    # Insert the operation into the database
    cursor.execute('INSERT INTO history (question, answer) VALUES (?, ?)', (math_expression, result))
    cursor.execute('''
        DELETE FROM history 
        WHERE id = (SELECT id FROM history ORDER BY id ASC LIMIT 1)
        AND (SELECT COUNT(*) FROM history) > 20
    ''')
    conn.commit()
    return jsonify({"question": math_expression, "answer": result})

@app.route('/history', methods=['GET'])
def get_history():
    # Retrieve the history from the database
    cursor.execute('SELECT question, answer FROM history ORDER BY id DESC LIMIT 20')
    history_from_db = cursor.fetchall()
    
    # Convert the result to a list of dictionaries
    history_list = [{"question": row[0], "answer": row[1]} for row in history_from_db]

    return jsonify(history_list)

if __name__ == '__main__':
    app.run(debug=True)
