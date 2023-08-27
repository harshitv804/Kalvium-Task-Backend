# Kalvium Task Backend
# Harshit V
# SRM Institute Of Science And Technology Ramapuram

from flask import Flask, request, jsonify

app = Flask(__name__)

cal_history = []

def calculate_expression(expression):
    try:
        return str(eval(expression)) 
    except:
        return "Invalid expression"

@app.route('/<path:expression>', methods=['GET'])
def perform_operation(expression):
    parts = expression.split('/')

    math_expression = ''.join(parts)

    result = calculate_expression(math_expression)

    # Add the operation to the history
    cal_history.append({"question": math_expression, "answer": result})

    if len(cal_history) > 20:
        cal_history.pop(0)

    return jsonify({"question": math_expression, "answer": result})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(cal_history)

if __name__ == '__main__':
    app.run(debug=True)