from shopify_api import shopify_graphql_request

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
