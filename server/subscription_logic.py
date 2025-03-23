from shopify_api import shopify_graphql_request

def get_customer_subscriptions(customer_id):
    query = """
    query GetSubscriptions($customerId: ID!) {
      subscriptionContracts(first: 10, customerId: $customerId) {
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
    """
    variables = {
        "customerId": f"gid://shopify/Customer/{customer_id}"
    }
    return shopify_graphql_request(query, variables)


def update_subscription(data):
    subscription_id = data.get("subscription_id")  # Must be full GID
    action = data.get("action")

    if not subscription_id or not action:
        return {"error": "Missing subscription_id or action"}, 400

    if action == "pause":
        query = """
        mutation subscriptionContractSetPause($id: ID!) {
          subscriptionContractSetPause(
            id: $id,
            pauseCollection: {
              behavior: MANUAL,
              resumeAt: null
            }
          ) {
            userErrors {
              field
              message
            }
          }
        }
        """
    elif action == "resume":
        query = """
        mutation subscriptionContractResume($id: ID!) {
          subscriptionContractResume(id: $id) {
            userErrors {
              field
              message
            }
          }
        }
        """
    elif action == "cancel":
        query = """
        mutation subscriptionContractCancel($id: ID!) {
          subscriptionContractCancel(id: $id) {
            userErrors {
              field
              message
            }
          }
        }
        """
    else:
        return {"error": "Unsupported action"}, 400

    variables = {"id": subscription_id}
    result = shopify_graphql_request(query, variables)
    return result
