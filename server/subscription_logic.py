# server/subscription_logic.py
from shopify_api import shopify_graphql_request

def get_customer_subscriptions(customer_id):
    query = """
    query GetSubscriptions($customerId: ID!) {
      customer(id: $customerId) {
        subscriptions(first: 10) {
          edges {
            node {
              id
              status
              nextBillingDate
              lines(first: 5) {
                edges {
                  node {
                    title
                    quantity
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "customerId": f"gid://shopify/Customer/{customer_id}"
    }
    result = shopify_graphql_request(query, variables)
    return result
