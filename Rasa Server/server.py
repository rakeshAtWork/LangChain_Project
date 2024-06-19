from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']

    # Simulated bot response (replace with your actual logic)
    bot_response = {
        'messages': [
            {'text': 'Hello! How can I help you today?'},
            {'text': 'This is a test response.'}
        ]
    }

    return jsonify(bot_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
