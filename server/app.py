from flask import Flask, request, jsonify
from subscription_logic import get_customer_subscriptions, update_subscription
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    customer_id = request.args.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'Missing customer_id'}), 400

    try:
        subscriptions = get_customer_subscriptions(customer_id)
        return jsonify(subscriptions)
    except Exception as e:
        logging.exception("Error in /subscriptions")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@app.route('/subscriptions/update', methods=['POST'])
def update_sub():
    try:
        data = request.json
        result = update_subscription(data)
        return jsonify(result)
    except Exception as e:
        logging.exception("Error in /subscriptions/update")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
