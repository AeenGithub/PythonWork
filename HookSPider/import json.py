import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/receiver/movie', methods=['POST'])
def receive():
    content = json.loads(request.data)
    print(content)
    # to something
    return jsonify({'status': True})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)