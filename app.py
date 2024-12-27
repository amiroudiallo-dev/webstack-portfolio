#!/usr/bin/python3
"""
Simple Flask API
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """
    Home route
    """
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route("/status", methods=["GET"])
def status():
    """
    Status route
    """
    return jsonify({"status": "API is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9440)

