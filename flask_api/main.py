from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify({"status": "online"})

if __name__ == "__main__":
    app.run(port=5000)
