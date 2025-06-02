from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__)

# In-memory message store (for demo; use a database for production)
messages = []

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    userName = data.get('userName', 'Anonymous')
    iconURL = data.get('iconURL', '')
    message = data.get('message', '')
    timestamp = time.time()
    msg = {
        'userName': userName,
        'iconURL': iconURL,
        'message': message,
        'timestamp': timestamp
    }
    messages.append(msg)
    return jsonify({'success': True})

@app.route('/api/get_messages')
def get_messages():
    since = float(request.args.get('since', 0))
    new_msgs = [m for m in messages if m['timestamp'] > since]
    return jsonify(new_msgs)

if __name__ == '__main__':
    app.run(debug=True)