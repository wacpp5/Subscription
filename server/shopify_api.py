# server/shopify_api.py
import requests
import os

SHOPIFY_SHOP = os.getenv("SHOPIFY_SHOP")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

def shopify_graphql_request(query, variables=None):
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "variables": variables or {}
    }

    response = requests.post(f"https://{SHOPIFY_SHOP}/admin/api/2024-01/graphql.json", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
