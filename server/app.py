# server/app.py
from flask import Flask, request, jsonify
from subscription_logic import get_customer_subscriptions, update_subscription
import os

app = Flask(__name__)

@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    customer_id = request.args.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'Missing customer_id'}), 400

    subscriptions = get_customer_subscriptions(customer_id)
    return jsonify(subscriptions)

@app.route('/subscriptions/update', methods=['POST'])
def update_sub():
    data = request.json
    result = update_subscription(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

